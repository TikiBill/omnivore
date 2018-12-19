""" Pixel converters

ByteValidator: change byte index list into rectangular grid
ColorIndexGenerator: bytes to pixel color indexes
PixelRenderer: pixel color indexes



Utility classes to convert byte representations of pixel data into
grids of color register indexes.

Color register indexes are byte values, each byte calculated from the integer
value of the bits making up the corresponding pixel. For example, Antic mode D
(graphics 7) uses 2 bits per pixel, laid out into 4 pixels:

  bit7 bit6 | bit5 bit4 | bit3 bit2 | bit1 bit0

where the color register indexes for each of the pixels is computed by:

  bit7*2 + bit6
  bit5*2 + bit4
  bit3*2 + bit2
  bit1*2 + bit0

Each byte would therefore contain values in the range of [0, 3].

This conversion is device independent; the code that displays pixels on screen will take these values and convert them to the color values referred to by these indexes.
"""
import numpy as np

from atrcopy import match_bit_mask, comment_bit_mask, selected_bit_mask, diff_bit_mask, user_bit_mask, not_user_bit_mask
ignore_mask = not_user_bit_mask & (0xff ^ diff_bit_mask)
invalid_style = 0xff

from omnivore_framework.utils.permute import bit_reverse_table


class ConverterBase:
    pixels_per_byte = 8
    bitplanes = 1

    @classmethod
    def validate_pixels_per_row(cls, pixels_per_row):
        return (pixels_per_row // cls.pixels_per_byte) * cls.pixels_per_byte

    @classmethod
    def calc_bytes_per_row(cls, pixels_per_row):
        return (pixels_per_row + cls.pixels_per_byte - 1) // cls.pixels_per_byte

    @classmethod
    def calc_grid_height(cls, num_byte_values, bytes_per_row):
        return (num_byte_values + bytes_per_row - 1) // bytes_per_row

    def calc_color_index_grid(self, byte_values, style, bytes_per_row):
        nr = len(byte_values) // bytes_per_row
        pixels = self.calc_pixels(byte_values, bytes_per_row)
        style_per_pixel = self.calc_style_per_pixel(pixels, style)
        return pixels.reshape((-1, bytes_per_row * self.pixels_per_byte)), style_per_pixel.reshape((-1, bytes_per_row * self.pixels_per_byte))


class Converter1bpp(ConverterBase):
    pixels_per_byte = 8

    def calc_pixels(self, byte_values, bytes_per_row):
        bits = np.unpackbits(byte_values)
        pixels = bits.reshape((-1, 8))
        return pixels

    def calc_style_per_pixel(self, pixels, style):
        h, w = pixels.shape
        stack = np.empty((len(style), 8), dtype=style.dtype)
        stack[:,0] = style
        stack[:,1] = style
        stack[:,2] = style
        stack[:,3] = style
        stack[:,4] = style
        stack[:,5] = style
        stack[:,6] = style
        stack[:,7] = style
        return stack.reshape((h, w))


class Converter2bpp(ConverterBase):
    pixels_per_byte = 4

    def calc_pixels(self, byte_values, bytes_per_row):
        bits = np.unpackbits(byte_values)
        bits = bits.reshape((-1, 8))
        pixels = np.empty((bits.shape[0], 4), dtype=np.uint8)
        pixels[:,0] = bits[:,0] * 2 + bits[:,1]
        pixels[:,1] = bits[:,2] * 2 + bits[:,3]
        pixels[:,2] = bits[:,4] * 2 + bits[:,5]
        pixels[:,3] = bits[:,6] * 2 + bits[:,7]
        return pixels

    def calc_style_per_pixel(self, pixels, style):
        h, w = pixels.shape
        stack = np.empty((len(style), 4), dtype=style.dtype)
        stack[:,0] = style
        stack[:,1] = style
        stack[:,2] = style
        stack[:,3] = style
        return stack.reshape((h, w))


class Converter4bpp(ConverterBase):
    pixels_per_byte = 2

    def calc_pixels(self, byte_values, bytes_per_row):
        bits = np.unpackbits(byte_values)
        bits = bits.reshape((-1, 8))
        pixels = np.empty((bits.shape[0], 2), dtype=np.uint8)
        pixels[:,0] = bits[:,0] * 8 + bits[:,1] * 4 + bits[:,2] * 2 + bits[:,3]
        pixels[:,1] = bits[:,4] * 8 + bits[:,5] * 4 + bits[:,6] * 2 + bits[:,7]
        return pixels

    def calc_style_per_pixel(self, pixels, style):
        h, w = pixels.shape
        stack = np.empty((len(style), 2), dtype=style.dtype)
        stack[:,0] = style
        stack[:,1] = style
        return stack.reshape((h, w))


class Converter8bpp(ConverterBase):
    pixels_per_byte = 1

    def calc_pixels(self, byte_values, bytes_per_row):
        return byte_values.reshape((-1, 1))

    def calc_style_per_pixel(self, pixels, style):
        h, w = pixels.shape
        style.reshape((h, w))
        return style

    def calc_valid_byte_grid(self, byte_values, style, grid_start_index, data_start_index, num_bytes, byte_width):
        num_prepend = max(data_start_index - grid_start_index, 0)
        _, num_extra = divmod(num_prepend + num_bytes, byte_width)
        if num_extra > 0:
            num_append = byte_width - num_extra
        else:
            num_append = 0
        if num_prepend + num_append > 0:
            total = num_prepend + num_append + num_bytes
            b = np.empty(total, dtype=byte_values.dtype)
            b[0:num_prepend] = 0
            b[num_prepend:num_prepend + num_bytes] = byte_values
            b[num_prepend + num_bytes:-1] = 0
            s[0:num_prepend] = 0
            s[num_prepend:num_prepend + num_bytes] = style
            s[num_prepend + num_bytes:-1] = 0
        else:
            b = byte_values
            s = style
        return b.reshape((-1, byte_width), s.reshape((-1, byte_width)))


class PixelRenderer:
    def to_rgb(self, color_indexes, style_per_pixel, colors, empty_color):
        h, w = color_indexes.shape
        color_indexes = color_indexes.reshape(-1)
        style_per_pixel = style_per_pixel.reshape(-1)
        flat_image = np.empty((h * w, 3), dtype=np.uint8)
        color_registers, h_colors, m_colors, c_colors, d_colors = colors
        for i in range(len(color_indexes)):
            color_index = color_indexes[i]
            style = style_per_pixel[i]
            if style == invalid_style:
                flat_image[i] = empty_color
            elif style & ignore_mask == 0:
                flat_image[i] = color_registers[color_index]
            elif style & selected_bit_mask:
                flat_image[i] = h_colors[color_index]
            elif (style & user_bit_mask) > 0:
                flat_image[i] = d_colors[color_index]
            elif style & comment_bit_mask:
                flat_image[i] = h_colors[color_index]
            elif style & match_bit_mask:
                flat_image[i] = h_colors[color_index]
            else:
                flat_image[i] = (0xff, 0, 0xee)  # not any of the above?
        return flat_image.reshape((h, w, 3))

    def reshape(self, bitimage, bytes_per_row, nr):
        # source array 'bitimage' in the shape of (size, w, 3)
        h, w, colors = bitimage.shape
        # create a new image with pixels in the correct aspect ratio
        output = bitimage.reshape((nr, self.pixels_per_byte * bytes_per_row, 3))
        output = intscale(output, self.scale_height, self.scale_width)
        log.debug("bitimage: %d,%d,%d; ppb=%d bpr=%d, output=%s" % (h, w, colors, self.pixels_per_byte * self.scale_width, bytes_per_row, str(output.shape)))
        return output
