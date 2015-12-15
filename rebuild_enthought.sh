#!/bin/bash

# Copy the enthought modules into the top-level directory so they are available
# in the omnivore package for pypi rather than as a set of dependencies that
# would require a complicated, install-it-yourself deal.  Upstream Enthought
# hasn't accepted my patches, and changing the names of the Enthought packages
# would require too many changes in too many places.  This is the best
# solution I could come up with -- at least this way, Omnivore doesn't have any
# external deps that can't be handled by pip (apart from wxPython 3.0).

REPOS="https://github.com/robmcmullen/traits.git https://github.com/robmcmullen/pyface.git https://github.com/robmcmullen/traitsui.git https://github.com/enthought/apptools.git https://github.com/robmcmullen/envisage.git"

TOPDIR=$PWD/enthought
mkdir -p $TOPDIR

for URL in $REPOS
do
    echo $URL
    echo $TOPDIR
    cd $TOPDIR
    REPO=`basename $URL`
    REPODIR=`basename -s .git $REPO`
    SUBDIR="$TOPDIR/$REPODIR"
    if [ -d $REPODIR ]
    then
        echo "Updating $REPO in $SUBDIR"
        cd $REPODIR
        git pull
    else
        echo "Cloning $REPO in $SUBDIR"
        cd $TOPDIR
        git clone $URL
    fi
    cd $TOPDIR/..
    ln -fs enthought/$REPODIR/$REPODIR
done
