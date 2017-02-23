import numpy as np

from errors import *
from segments import SegmentData, EmptySegment, ObjSegment, RawSectorsSegment
from utils import *

import logging
log = logging.getLogger(__name__)


class BaseHeader(object):
    file_format = "generic"  # text descriptor of file format
    sector_class = WriteableSector

    def __init__(self, sector_size=256, initial_sectors=0, vtoc_sector=0, starting_sector_label=0):
        self.image_size = 0
        self.sector_size = sector_size
        self.initial_sector_size = 0
        self.num_initial_sectors = 0
        self.crc = 0
        self.unused = 0
        self.flags = 0
        self.header_offset = 0
        self.starting_sector_label = starting_sector_label
        self.max_sectors = 0  # number of sectors, -1 is unlimited
        self.tracks_per_disk = 0
        self.sectors_per_track = 0
        self.first_vtoc = vtoc_sector
        self.num_vtoc = 1
        self.extra_vtoc = []
        self.first_directory = 0
        self.num_directory = 0
    
    def __len__(self):
        return self.header_offset
    
    def to_array(self):
        header_bytes = np.zeros([self.header_offset], dtype=np.uint8)
        self.encode(header_bytes)
        return header_bytes

    def encode(self, header_bytes):
        """Subclasses should override this to put the byte values into the
        header.
        """
        return

    def sector_is_valid(self, sector):
        return (self.max_sectors < 0) | (sector >= self.starting_sector_label and sector < (self.max_sectors + self.starting_sector_label))
    
    def get_pos(self, sector):
        """Get index (into the raw data of the disk image) of start of sector

        This base class method assumes the sectors are one after another, in
        order starting from the beginning of the raw data.
        """
        if not self.sector_is_valid(sector):
            raise ByteNotInFile166("Sector %d out of range" % sector)
        pos = sector * self.sector_size + self.header_offset
        size = self.sector_size
        return pos, size

    def sector_from_track(self, track, sector):
        return (track * self.sectors_per_track) + sector

    def track_from_sector(self, sector):
        track, sector = divmod(sector, self.sectors_per_track)
        return track, sector

    def check_size(self, size):
        raise InvalidDiskImage("BaseHeader subclasses need custom checks for size")

    def strict_check(self, image):
        pass

    def create_sector(self, data):
        return self.sector_class(self.sector_size, data)



class AtrHeader(BaseHeader):
    # ATR Format described in http://www.atarimax.com/jindroush.atari.org/afmtatr.html
    format = np.dtype([
        ('wMagic', '<u2'),
        ('wPars', '<u2'),
        ('wSecSize', '<u2'),
        ('btParsHigh', 'u1'),
        ('dwCRC','<u4'),
        ('unused','<u4'),
        ('btFlags','u1'),
        ])
    file_format = "ATR"
    
    def __init__(self, bytes=None, sector_size=128, initial_sectors=3, create=False):
        BaseHeader.__init__(self, sector_size, initial_sectors, 360)
        if create:
            self.header_offset = 16
            self.check_size(0)
        if bytes is None:
            return
        
        if len(bytes) == 16:
            values = bytes.view(dtype=self.format)[0]
            if values[0] != 0x296:
                raise InvalidAtrHeader
            self.image_size = (int(values[3]) * 256 * 256 + int(values[1])) * 16
            self.sector_size = int(values[2])
            self.crc = int(values[4])
            self.unused = int(values[5])
            self.flags = int(values[6])
            self.header_offset = 16
        else:
            raise InvalidAtrHeader
    
    def __str__(self):
        return "%s Disk Image (size=%d (%dx%db), crc=%d flags=%d unused=%d)" % (self.file_format, self.image_size, self.max_sectors, self.sector_size, self.crc, self.flags, self.unused)
    
    def encode(self, raw):
        values = raw.view(dtype=self.format)[0]
        values[0] = 0x296
        paragraphs = self.image_size / 16
        parshigh, pars = divmod(paragraphs, 256*256)
        values[1] = pars
        values[2] = self.sector_size
        values[3] = parshigh
        values[4] = self.crc
        values[5] = self.unused
        values[6] = self.flags
        return raw

    def check_size(self, size):
        if size == 92160 or size == 92176:
            self.image_size = 92160
            self.sector_size = 128
            self.initial_sector_size = 0
            self.num_initial_sectors = 0
        elif size == 184320 or size == 184336:
            self.image_size = 184320
            self.sector_size = 256
            self.initial_sector_size = 0
            self.num_initial_sectors = 0
        elif size == 183936 or size == 183952:
            self.image_size = 183936
            self.sector_size = 256
            self.initial_sector_size = 128
            self.num_initial_sectors = 3
        else:
            self.image_size = size
        self.first_vtoc = 360
        self.num_vtoc = 1
        self.first_directory = 361
        self.num_directory = 8
        self.tracks_per_disk = 40
        self.sectors_per_track = 18
        initial_bytes = self.initial_sector_size * self.num_initial_sectors
        self.max_sectors = ((self.image_size - initial_bytes) / self.sector_size) + self.num_initial_sectors
    
    def get_pos(self, sector):
        if not self.sector_is_valid(sector):
            raise ByteNotInFile166("Sector %d out of range" % sector)
        if sector <= self.num_initial_sectors:
            pos = self.num_initial_sectors * (sector - 1)
            size = self.initial_sector_size
        else:
            pos = self.num_initial_sectors * self.initial_sector_size + (sector - 1 - self.num_initial_sectors) * self.sector_size
            size = self.sector_size
        pos += self.header_offset
        return pos, size


class XfdHeader(AtrHeader):
    file_format = "XFD"
    
    def __str__(self):
        return "%s Disk Image (size=%d (%dx%db)" % (self.file_format, self.image_size, self.max_sectors, self.sector_size)
    
    def __len__(self):
        return 0
    
    def to_array(self):
        raw = np.zeros([0], dtype=np.uint8)
        return raw

    def strict_check(self, image):
        size = len(image)
        if size in [92160, 133120, 183936, 184320]:
            return
        raise InvalidDiskImage("Uncommon size of XFD file")


class DiskImageBase(object):
    def __init__(self, rawdata, filename=""):
        self.rawdata = rawdata
        self.bytes = self.rawdata.get_data()
        self.style = self.rawdata.get_style()
        self.size = np.alen(self.bytes)
        self.set_filename(filename)
        self.header = None
        self.total_sectors = 0
        self.unused_sectors = 0
        self.files = [] # all dirents that show up in a normal dir listing
        self.segments = []
        self.all_sane = True
        self.setup()

    def __len__(self):
        return len(self.rawdata)

    @property
    def bytes_per_sector(self):
        raise NotImplementedError

    @property
    def payload_bytes_per_sector(self):
        raise NotImplementedError

    @property
    def writeable_sector_class(self):
        return WriteableSector

    @property
    def raw_sector_class(self):
        return RawSectorsSegment

    @property
    def vtoc_class(self):
        return VTOC

    @property
    def directory_class(self):
        return Directory

    @property
    def sector_builder_class(self):
        return SectorBuilder
    
    def set_filename(self, filename):
        if "." in filename:
            self.filename, self.ext = filename.rsplit(".", 1)
        else:
            self.filename, self.ext = filename, ""
    
    def dir(self):
        lines = []
        lines.append(str(self))
        for dirent in self.files:
            if dirent.in_use:
                lines.append(str(dirent))
        return "\n".join(lines)

    def setup(self):
        self.size = np.alen(self.bytes)
        self.read_header()
        self.header.check_size(self.size - len(self.header))
        self.check_size()
        self.get_metadata()

    def get_metadata(self):
        self.get_boot_sector_info()
        self.get_vtoc()
        self.get_directory()
        self.check_sane()

    def strict_check(self):
        """Perform the strictest of checks to verify the data is valid """
        self.header.strict_check(self)

    def relaxed_check(self):
        """Conform as much as possible to get the data to work with this
        format.
        """
        pass
    
    @classmethod
    def new_header(cls, diskimage, format="ATR"):
        if format.lower() == "atr":
            header = AtrHeader(create=True)
            header.check_size(diskimage.size)
        else:
            raise RuntimeError("Unknown header type %s" % format)
        return header
    
    def as_new_format(self, format="ATR"):
        """ Create a new disk image in the specified format
        """
        first_data = len(self.header)
        raw = self.rawdata[first_data:]
        data = add_atr_header(raw)
        newraw = SegmentData(data)
        image = self.__class__(newraw)
        return image
    
    def save(self, filename=""):
        if not filename:
            filename = self.filename
            if self.ext:
                filename += "." + self.ext
        if not filename:
            raise RuntimeError("No filename specified for save!")
        bytes = self.bytes[:]
        with open(filename, "wb") as fh:
            bytes.tofile(fh)
    
    def assert_valid_sector(self, sector):
        if not self.header.sector_is_valid(sector):
            raise ByteNotInFile166("Sector %d out of range" % sector)
    
    def check_sane(self):
        if not self.all_sane:
            raise InvalidDiskImage("Invalid directory entries; may be boot disk")
    
    def read_header(self):
        bytes = self.bytes[0:16]
        try:
            self.header = AtrHeader(bytes)
        except InvalidAtrHeader:
            self.header = XfdHeader()
    
    def check_size(self):
        pass
    
    def get_boot_sector_info(self):
        pass
    
    def get_vtoc(self):
        """Get information from VTOC and populate the VTOC object"""
        pass
    
    def get_directory(self, directory=None):
        pass
    
    def get_raw_bytes(self, sector):
        pos, size = self.header.get_pos(sector)
        return self.bytes[pos:pos + size], pos, size
    
    def get_sector_slice(self, start, end=None):
        """ Get contiguous sectors
        
        :param start: first sector number to read (note: numbering starts from 1)
        :param end: last sector number to read
        :returns: bytes
        """
        pos, size = self.header.get_pos(start)
        if end is None:
            end = start
        while start < end:
            start += 1
            _, more = self.header.get_pos(start)
            size += more
        return slice(pos, pos + size)
    
    def get_sectors(self, start, end=None):
        """ Get contiguous sectors
        
        :param start: first sector number to read (note: numbering starts from 1)
        :param end: last sector number to read
        :returns: bytes
        """
        s = self.get_sector_slice(start, end)
        return self.bytes[s], self.style[s]
    
    def get_contiguous_sectors(self, sector, num):
        start = 0
        count = 0
        for index in range(sector, sector + num):
            pos, size = self.header.get_pos(index)
            if start == 0:
                start = pos
            count += size
        return start, count
    
    def parse_segments(self):
        r = self.rawdata
        i = self.header.header_offset
        if self.header.image_size > 0:
            self.segments.append(ObjSegment(r[0:i], 0, 0, 0, i, name="%s Header" % self.header.file_format))
        self.segments.append(self.raw_sector_class(r[i:], self.header.starting_sector_label, self.header.max_sectors, self.header.image_size, self.header.initial_sector_size, self.header.num_initial_sectors, self.header.sector_size, name="Raw disk sectors"))
        self.segments.extend(self.get_boot_segments())
        self.segments.extend(self.get_vtoc_segments())
        self.segments.extend(self.get_directory_segments())
        self.segments.extend(self.get_file_segments())
    
    boot_record_type = np.dtype([
        ('BFLAG', 'u1'),
        ('BRCNT', 'u1'),
        ('BLDADR', '<u2'),
        ('BWTARR', '<u2'),
        ])
    
    def get_boot_segments(self):
        data, style = self.get_sectors(1)
        values = data[0:6].view(dtype=self.boot_record_type)[0]  
        flag = int(values[0])
        segments = []
        if flag == 0:
            num = int(values[1])
            addr = int(values[2])
            s = self.get_sector_slice(1, num)
            r = self.rawdata[s]
            header = ObjSegment(r[0:6], 0, 0, addr, addr + 6, name="Boot Header")
            sectors = ObjSegment(r, 0, 0, addr, addr + len(r), name="Boot Sectors")
            code = ObjSegment(r[6:], 0, 0, addr + 6, addr + len(r), name="Boot Code")
            segments = [sectors, header, code]
        return segments
    
    def get_vtoc_segments(self):
        return []

    def get_directory_segments(self):
        return []
    
    def find_dirent(self, filename):
        for dirent in self.files:
            if filename == dirent.get_filename():
                return dirent
        raise FileNotFound("%s not found on disk" % filename)
    
    def find_file(self, filename):
        dirent = self.find_dirent(filename)
        return self.get_file(dirent)
    
    def get_file(self, dirent):
        segment = self.get_file_segment(dirent)
        return segment.tostring()
    
    def get_file_segment(self, dirent):
        pass
    
    def get_file_segments(self):
        segments = []
        for dirent in self.files:
            try:
                segment = self.get_file_segment(dirent)
            except InvalidFile, e:
                segment = EmptySegment(self.rawdata, name=dirent.get_filename(), error=str(e))
            segments.append(segment)
        return segments

    # file writing methods

    def begin_transaction(self):
        state = self.bytes[:], self.style[:]
        return state

    def rollback_transaction(self, state):
        self.bytes[:], self.style[:] = state
        return

    def write_file(self, filename, filetype, data):
        """Write data to a file on disk

        This throws various exceptions on failures, for instance if there is
        not enough space on disk or a free entry is not available in the
        catalog.
        """
        state = self.begin_transaction()
        try:
            directory = self.directory_class(self.header)
            self.get_directory(directory)
            dirent = directory.add_dirent(filename, filetype)
            data = to_numpy(data)
            sector_list = self.sector_builder_class(self.header, self.payload_bytes_per_sector, data, self.writeable_sector_class)
            vtoc_segments = self.get_vtoc_segments()
            vtoc = self.vtoc_class(self.bytes_per_sector, vtoc_segments)
            directory.save_dirent(self, dirent, vtoc, sector_list)
            self.write_sector_list(sector_list)
            self.write_sector_list(vtoc)
            self.write_sector_list(directory)
            self.get_metadata()
        except AtrError:
            self.rollback_transaction(state)
            raise
        finally:
            self.get_metadata()

    def write_sector_list(self, sector_list):
        for sector in sector_list:
            pos, size = self.header.get_pos(sector.sector_num)
            log.debug("writing: %s" % sector)
            self.bytes[pos:pos + size] = sector.data

    def delete_file(self, filename):
        state = self.begin_transaction()
        try:
            directory = self.directory_class(self.header)
            self.get_directory(directory)
            dirent = directory.find_dirent(filename)
            sector_list = dirent.get_sector_list(self)
            vtoc_segments = self.get_vtoc_segments()
            vtoc = self.vtoc_class(self.header, vtoc_segments)
            directory.remove_dirent(self, dirent, vtoc, sector_list)
            self.write_sector_list(sector_list)
            self.write_sector_list(vtoc)
            self.write_sector_list(directory)
            self.get_metadata()
        except AtrError:
            self.rollback_transaction(state)
            raise
        finally:
            self.get_metadata()



class BootDiskImage(DiskImageBase):
    def __str__(self):
        return "%s Boot Disk" % (self.header)
    
    def check_size(self):
        if self.header is None:
            return
        start, size = self.header.get_pos(1)
        b = self.bytes
        i = self.header.header_offset
        flag = b[i:i + 2].view(dtype='<u2')[0]
        if flag == 0xffff:
            raise InvalidDiskImage("Appears to be an executable")
        nsec = b[i + 1]
        bload = b[i + 2:i + 4].view(dtype='<u2')[0]
        
        # Sanity check: number of sectors to be loaded can't be more than the
        # lower 48k of ram because there's no way to bank switch or anything
        # before the boot sectors are finished loading
        max_ram = 0xc000
        max_size = max_ram - bload
        max_sectors = max_size / self.header.sector_size
        if nsec > max_sectors or nsec < 1:
            raise InvalidDiskImage("Number of boot sectors out of range")
        if bload < 0x200 or bload > (0xc000 - (nsec * self.header.sector_size)):
            raise InvalidDiskImage("Bad boot load address")

def add_atr_header(bytes):
    header = AtrHeader(create=True)
    header.check_size(len(bytes))
    hlen = len(header)
    data = np.empty([hlen + len(bytes)], dtype=np.uint8)
    data[0:hlen] = header.to_array()
    data[hlen:] = bytes
    return data
