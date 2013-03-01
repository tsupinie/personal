
import struct

import numpy as np

class DoradeFile:
    def __init__(self, file_name, mode):
        self._defaults = []
        self._dorade = open(file_name, mode)

        self._defaults = dir(self)

        if 'r' in mode:
            self._readHeaders()
            self._readSweep()
        return

    def _readHeaders(self):

        self._readSuperSweepIDBlock()
        self._readVolumeDescriptor()
        self._readSensorDescriptors(self.num_sens_descr)        
        return

    def _readSuperSweepIDBlock(self):
        _marker = self._read('s4')
        if _marker != "SSWB": 
            print "Error: Expected volume descriptor marker (SSWB)"

        super_sweep_id_block_length = self._read('i')
        self.last_used              = self._read('i')
        self.start_time             = self._read('i')
        self.stop_time              = self._read('i')

        file_size                   = self._read('i')

        self.compression_flag       = self._read('i')
        self.volume_time_stamp      = self._read('i')
        self.num_params             = self._read('i')
        self.radar_name             = self._read('s8')

        start_time                  = self._read('d')
        stop_time                   = self._read('d')

        self.version_number         = self._read('i')
        num_key_tables              = self._read('i')

        status                      = self._read('i')

        for idx in range(7):
            placeholder             = self._read('i')

        self.key_table = []
        for idx in range(8):
            key = {}

            key['offset']           = self._read('i')
            key['size']             = self._read('i')
            key['type']             = self._read('i')

            self.key_table.append(key)

        return

    def _readVolumeDescriptor(self):
        _marker = self._read('s4')
        if _marker != "VOLD": 
            print "Error: Expected volume descriptor marker (VOLD)"

        _vol_descr_length      = self._read('i')
        self.revision_number   = self._read('h')
        self.volume_number     = self._read('h')
        self.max_record_length = self._read('i')
        self.project_name      = self._read('s20')

        self.year_data         = self._read('h')
        self.month_data        = self._read('h')
        self.day_data          = self._read('h')
        self.hour_data         = self._read('h')
        self.minute_data       = self._read('h')
        self.second_data       = self._read('h')

        self.flight_number     = self._read('s8')
        self.record_source_id  = self._read('s8')

        self.year_recording    = self._read('h')
        self.month_recording   = self._read('h')
        self.day_recording     = self._read('h')

        self.num_sens_descr    = self._read('h')
        return

    def _readSensorDescriptors(self, n_sensor_descr):
        self.radar_descriptors = []
        for sens_descr in range(n_sensor_descr):
            descriptor = {}

            _marker = self._read('s4')
            if _marker != "RADD": 
                print "Error: Expected sensor descriptor marker (RADD)"

            descriptor_length              = self._read('i')
            descriptor['name']             = self._read('s8')
            descriptor['radar_constant']   = self._read('f')
            descriptor['peak_power']       = self._read('f')
            descriptor['noise_power']      = self._read('f')
            descriptor['receiver_gain']    = self._read('f')
            descriptor['antenna_gain']     = self._read('f')
            descriptor['system_gain']      = self._read('f')
            descriptor['horiz_beam_width'] = self._read('f')
            descriptor['vert_beam_width']  = self._read('f')
 
            descriptor['radar_type']       = self._read('h')   
            descriptor['scan_mode']        = self._read('h')

            descriptor['antenna_rot_vel']  = self._read('f')
            descriptor['scan_param_1']     = self._read('f')
            descriptor['scan_param_2']     = self._read('f')

            num_param_descr                = self._read('h')
            num_additional_descr           = self._read('h')

            data_compression               = self._read('h')
            data_reduction                 = self._read('h')
            data_reduction_param_1         = self._read('f')
            data_reduction_param_2         = self._read('f')

            descriptor['radar_longitude']  = self._read('f')
            descriptor['radar_latitude']   = self._read('f')
            descriptor['radar_altitude']   = self._read('f')

#           print descriptor['radar_longitude']
#           print descriptor['radar_latitude']
#           print descriptor['radar_altitude']

            descriptor['unambig_velocity'] = self._read('f')
            descriptor['unambig_range']    = self._read('f')

            num_frequencies                = self._read('h')
            num_interpulse_per             = self._read('h')

            descriptor['frequencies']      = self._read('fffff')
            descriptor['interpulse_per']   = self._read('fffff')

            descriptor['parameters']       = self._readParameterDescriptors(num_param_descr)
            descriptor['cell_range_vec']   = self._readCellRangeVector()
            descriptor['corr_factor']      = self._readCorrectionFactorDescriptor()

            self.radar_descriptors.append(descriptor)

        return

    def _readParameterDescriptors(self, n_parameter_descr):
        parameter_descriptors = []

        for parm_desc in range(n_parameter_descr):
            descriptor = {}

            _marker = self._read('s4')
            if _marker != "PARM": 
                print "Error: Expected parameter descriptor marker (PARM)"

            param_descr_length               = self._read('i')

            descriptor['name']               = self._read('s8')
            descriptor['description']        = self._read('s40')
            descriptor['units']              = self._read('s8')

            descriptor['interpulse_used']    = self._read('h')
            descriptor['frequency_used']     = self._read('h')

            descriptor['receiver_bandwidth'] = self._read('f')
            descriptor['pulse_width']        = self._read('h')
            descriptor['polarization']       = self._read('h')
            descriptor['num_samples']        = self._read('h')
            descriptor['binary_format']      = self._read('h')

            descriptor['threshold_param']    = self._read('s8')
            descriptor['thershold_value']    = self._read('f')

            descriptor['scale_factor']       = self._read('f')
            descriptor['bias_factor']        = self._read('f')

            descriptor['bad_data_flag']      = self._read('i')

            print descriptor['name']

            parameter_descriptors.append(descriptor)

        return parameter_descriptors

    def _readCellRangeVector(self):
        _marker = self._read('s4')
        if _marker != "CELV": 
            print "Error: Expected cell range vector marker (CELV)"

        comment_length     = self._read('i')
        cell_vector_length = self._read('i')
        cell_vector        = self._read('f' * 1500) # is 1500 constant for all files?

        return cell_vector

    def _readCorrectionFactorDescriptor(self):
        descriptor = {}
        _marker = self._read('s4')
        if _marker != "CFAC": 
            print "Error: Expected correction factor descriptor marker (CFAC)"

        corr_fact_descr_length         = self._read('i')
        descriptor['azimuth']          = self._read('f')
        descriptor['elevation']        = self._read('f')
        descriptor['range_delay']      = self._read('f')
        descriptor['longitude']        = self._read('f')
        descriptor['latitude']         = self._read('f')
        descriptor['pressure_alt']     = self._read('f')
        descriptor['physical_alt']     = self._read('f')
        descriptor['platform_u']       = self._read('f')
        descriptor['platform_v']       = self._read('f')
        descriptor['platform_w']       = self._read('f')
        descriptor['platform_heading'] = self._read('f')
        descriptor['platform_roll']    = self._read('f')
        descriptor['platform_pitch']   = self._read('f')
        descriptor['platform_drift']   = self._read('f')
        descriptor['rotation_angle']   = self._read('f')
        descriptor['tilt_angle']       = self._read('f')

        return descriptor

    def _readSweep(self):
        self._readSweepDescriptor()
        self._readRays(self.num_rays, self.radar_descriptors[0]['parameters'])
        return

    def _readSweepDescriptor(self):
        
        _marker = self._read('s4')
        if _marker != "SWIB": 
            print "Error: Expected sweep descriptor marker (SWIB)"

        sweep_descr_length    = self._read('i')
        sweep_comment         = self._read('s8')
        sweep_number          = self._read('i')
        self.num_rays         = self._read('i')
        self.true_start_angle = self._read('f')
        self.true_end_angle   = self._read('f')
        fixed_angle           = self._read('f')
        filter_flag           = self._read('i')

        return

    def _readRays(self, n_rays, parameter_descriptors):
        self._rays = []

        for ray in range(n_rays):
            descriptor = {}
            descriptor['ray_info']      = self._readRayInfoBlock()
            descriptor['platform_info'] = self._readPlatformInfoBlock()

            descriptor['param_data']    = {}
            for param_desc in parameter_descriptors:
                _marker = self._read('s4')
                if _marker != "RDAT":
                    print "Error: Expected radar data marker (RDAT): ray %d" % ray
                radar_data_length = self._read('i')
                parameter_name = self._read('s8')

                if parameter_name != param_desc['name']:
                    print "Error: Expected parameter %s, but got %s" % (param_desc['name'], parameter_name)

                data_type = {1:'b', 2:'h', 3:'i', 4:'f'}[ param_desc['binary_format'] ]
                data_width = {1:1, 2:2, 3:4, 4:4}[ param_desc['binary_format'] ]
                data_compressed = np.array(self._read(data_type * ((radar_data_length - 16) / data_width)))

                data = self._decompressHRD(data_compressed)#, debug=(ray == 0))
                data = self._remap(data, param_desc)
                descriptor['param_data'][parameter_name] = data

            self._rays.append(descriptor)
        return

    def _decompressHRD(self, compressed_data, debug=False):
        decompressed_data = []
        idx = 0

        if debug:
            print compressed_data

        while idx < len(compressed_data) and compressed_data[idx] != 1:

            count = compressed_data[idx] & int("0x7fff", 0)
            good_data = compressed_data[idx] & int("0x8000", 0)

            if debug:
                print count, bool(good_data)

            if good_data:
                decompressed_data.extend(compressed_data[(idx + 1):(idx + count + 1)])
                idx += count + 1
            else:
                decompressed_data.extend([ -int("0x8000", 0) for jdy in range(count) ])
                idx += 1

        return np.array(decompressed_data)

    def _remap(self, data, parameter_desc):
        return np.where(data > -10000, data / parameter_desc['scale_factor'] - parameter_desc['bias_factor'], data)

    def _readRayInfoBlock(self):
        descriptor = {}
        _marker = self._read('s4')
        if _marker != "RYIB": 
            print "Error: Expected ray info block marker (RYIB)"

        ray_info_block_length       = self._read('i')
        descriptor['sweep_number']  = self._read('i')
        descriptor['julian_day']    = self._read('i')
        descriptor['hour']          = self._read('h')
        descriptor['minute']        = self._read('h')
        descriptor['second']        = self._read('h')
        descriptor['millisecond']   = self._read('h')
        descriptor['azimuth']       = self._read('f')
        descriptor['elevation']     = self._read('f')
        descriptor['peak_tx_power'] = self._read('f')
        descriptor['scan_rate']     = self._read('f')
        descriptor['ray_status']    = self._read('i')

        return descriptor

    def _readPlatformInfoBlock(self):
        descriptor = {}

        _marker = self._read('s4')
        if _marker != "ASIB": 
            print "Error: Expected platform info block marker (ASIB)"

        platform_info_block_length     = self._read('i')
        descriptor['longitude']        = self._read('f')
        descriptor['latitude']         = self._read('f')
        descriptor['altitude_msl']     = self._read('f')
        descriptor['altitude_agl']     = self._read('f')
        descriptor['antenna_u']        = self._read('f')
        descriptor['antenna_v']        = self._read('f')
        descriptor['antenna_w']        = self._read('f')
        descriptor['heading']          = self._read('f')
        descriptor['roll']             = self._read('f')
        descriptor['pitch']            = self._read('f')
        descriptor['drift']            = self._read('f')
        descriptor['beam_sweep_angle'] = self._read('f')
        descriptor['beam_scan_angle']  = self._read('f')
        descriptor['air_u']            = self._read('f')
        descriptor['air_v']            = self._read('f')
        descriptor['air_w']            = self._read('f')
        descriptor['heading_chg_rate'] = self._read('f')
        descriptor['pitch_chg_rate']   = self._read('f')

        return descriptor

    def _read(self, type_string):
        if type_string[0] != 's':
            size = struct.calcsize(type_string)
            data = struct.unpack("<%s" % type_string, self._dorade.read(size))
        else:
            size = int(type_string[1:])
            data = tuple([ self._dorade.read(size).strip("\0") ])

        if len(data) == 1:
            return data[0]
        else:
            return list(data)

    def getSweep(self, parameter_name):
        sweep = np.empty((self.num_rays, len(self._rays[0]['param_data'][parameter_name])))
        for idx in range(self.num_rays):
            sweep[idx] = self._rays[idx]['param_data'][parameter_name]

        return sweep

def open_file(file_name, mode):
    return DoradeFile(file_name, mode)

if __name__ == "__main__":
    dor = open_file("swp.1090605194442.KFTG.486.0.5_SUR_v531", 'r')
    print dor.getSweep("REF").max()
