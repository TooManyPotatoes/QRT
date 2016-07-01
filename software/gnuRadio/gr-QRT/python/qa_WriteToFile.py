#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from WriteToFile import WriteToFile
import h5py
import numpy as np
import datetime as dt
import scipy.signal as sp
from welch import welch

class qa_WriteToFile (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        def generate(inputs):
            fs = 10000.0
            f1 = 1234.0
            amp1 = 2*np.sqrt(2)
            f2 = 2500.2157
            amp2 = 1.
            ulsb = 1.e-3
            t = np.arange(inputs) / fs
            waves = amp1*np.sin(t*(2*np.pi)*f1)+amp2*np.sin(t*(2*np.pi)*f2)
            noise = np.floor(waves/ulsb+.5)*ulsb
            data = waves + noise
            return data
        rdata = generate(10000)
        idata = np.zeros(len(rdata))*1j
        src_data = np.add(rdata,idata)
        nf = 1024
	fs = 10000
	scale = 'density'
        nperseg = nf
        item_size = np.dtype("complex64").itemsize
        tname = '0'
        nData = len(src_data)
        date = dt.datetime.today()
        filename = str(tname) + str(date.year) + str(date.month) + str(date.day) + str(date.hour) + '.hdf5'
        f = h5py.File(filename, 'a')
        subgroup = 'test'
        subgroup1 = str(date.minute)
        dset_name = str(date.second)
        freq, power = sp.welch(src_data,fs=10000,
                          window='hann',nperseg=nperseg,
                          noverlap=nf*.5,scaling=scale,detrend=False,return_onesided=False)
        time = (date.year,date.month,date.day,date.hour,date.minute,date.second)
        power = np.add(power,np.zeros(len(power))*1.j)
        if subgroup1+'/test' in f:
            dset = f[subgroup1+'/test']
            dset.attrs['date'] = time
            dset.attrs['telescope'] = tname
            dset = dset[...] + power[...]
        else:
            dset = f.create_dataset(subgroup1+'/test',data=power)
            dset.attrs['date'] = time
            dset.attrs['telescope'] = tname
        s2v = blocks.stream_to_vector(item_size, nData)
	src = blocks.vector_source_c(src_data)
	wel = welch(nData, scale, nf, fs, .5)
	fil = WriteToFile(tname, nf)
	self.tb.connect(src, s2v)
        self.tb.connect(s2v, wel)
	self.tb.connect(wel, fil)
	self.tb.run ()
        result = f[subgroup1+'/'+dset_name]
        expected_result = f[subgroup1+'/test']
	self.assertFloatTuplesAlmostEqual(expected_result[...], result[...])

if __name__ == '__main__':
    gr_unittest.run(qa_WriteToFile, "qa_WriteToFile.xml")
