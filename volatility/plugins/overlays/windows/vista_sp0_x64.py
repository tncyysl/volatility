# Volatility
# Copyright (c) 2008 Volatile Systems
# Copyright (c) 2008 Brendan Dolan-Gavitt <bdolangavitt@wesleyan.edu>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details. 
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA 
#

"""
@author:       Bradley L Schatz
@license:      GNU General Public License 2.0 or later
@contact:      bradley@schatzforensic.com.au

This file provides support for windows XP SP3. We provide a profile
for SP3.
"""

#pylint: disable-msg=C0111

import copy
import vista_sp0_x64_vtypes
import vista_sp0_x64_syscalls
import win2k3_sp2_x64
import windows
import windows64
import tcpip_vtypes
import crash_vtypes
import hibernate_vtypes
import kdbg_vtypes
import ssdt_vtypes
import pe_vtypes
import volatility.debug as debug #pylint: disable-msg=W0611

overlay = copy.deepcopy(win2k3_sp2_x64.overlay)

object_classes = copy.deepcopy(win2k3_sp2_x64.object_classes)

vtypes = copy.deepcopy(vista_sp0_x64_vtypes.ntkrnlmp_types)

overlay['VOLATILITY_MAGIC'][1]['DTBSignature'][1] = ['VolatilityMagic', dict(value = "\x03\x00\x30\x00")]
overlay['VOLATILITY_MAGIC'][1]['KDBGHeader'][1] = ['VolatilityMagic', dict(value = '\x00\xf8\xff\xffKDBG\x28\x03')]

vtypes.update(crash_vtypes.crash_vtypes)
vtypes.update(hibernate_vtypes.hibernate_vtypes)
vtypes.update(kdbg_vtypes.kdbg_vtypes)
vtypes.update(tcpip_vtypes.tcpip_vtypes_vista)
vtypes.update(ssdt_vtypes.ssdt_vtypes_64)
vtypes.update(pe_vtypes.pe_vtypes)
vtypes.update(pe_vtypes.pe_vtypes_64)

# Alias _IMAGE_NT_HEADERS for 64-bit systems
vtypes["_IMAGE_NT_HEADERS"] = vtypes["_IMAGE_NT_HEADERS64"]

class VistaSP0x64(windows64.AbstractWindowsX64):
    """ A Profile for Windows Vista SP0 x64 """
    _md_major = 6
    _md_minor = 0
    overlay = overlay
    abstract_types = vtypes
    object_classes = object_classes
    syscalls = vista_sp0_x64_syscalls.syscalls

class _MMVAD_SHORT(windows._MMVAD_SHORT):
    def get_parent(self):
        return self.u1.Parent

    def get_control_area(self):
        return self.Subsection.ControlArea

    def get_file_object(self):
        return self.Subsection.ControlArea.FilePointer.dereference_as("_FILE_OBJECT")

class _MMVAD_LONG(_MMVAD_SHORT):
    pass

class _ETHREAD(windows._ETHREAD):
    """A class for Windows 7 ETHREAD objects"""

    def owning_process(self):
        """Return the EPROCESS that owns this thread"""
        return self.Tcb.Process.dereference_as("_EPROCESS")

object_classes['_MMVAD_SHORT'] = _MMVAD_SHORT
object_classes['_MMVAD_LONG'] = _MMVAD_LONG
object_classes['_ETHREAD'] = _ETHREAD
