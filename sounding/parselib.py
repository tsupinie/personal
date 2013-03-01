
import numpy as np

import cPickle

def qualityControl(snd, *values, **kwargs):
    if 'uv' not in kwargs:
        kwargs['uv'] = True

    u_obs_snd  = snd['u_wind']
    v_obs_snd  = snd['v_wind']
    t_obs_snd  = snd['temperature']
    td_obs_snd = snd['dewpoint']
    p_obs_snd  = snd['pressure']

    if kwargs['uv']:
        u_miss_value, v_miss_value, t_miss_value, td_miss_value, p_miss_value = values
        good = (u_obs_snd != u_miss_value) & (v_obs_snd != v_miss_value) & (t_obs_snd != t_miss_value) & (td_obs_snd != td_miss_value) & (p_obs_snd != p_miss_value)
    else:
        wd_obs_snd  = snd['wind_dir']
        ws_obs_snd  = snd['wind_spd']

        wd_miss_value, ws_miss_value, t_miss_value, td_miss_value, p_miss_value = values
        good = (wd_obs_snd != wd_miss_value) & (ws_obs_snd != ws_miss_value) & (t_obs_snd != t_miss_value) & (td_obs_snd != td_miss_value) & (p_obs_snd != p_miss_value)

    good_idxs = np.where(good)[0]

    snd['u_wind']      = u_obs_snd[good_idxs]
    snd['v_wind']      = v_obs_snd[good_idxs]
    snd['temperature'] = t_obs_snd[good_idxs]
    snd['dewpoint']    = td_obs_snd[good_idxs]
    snd['pressure']    = p_obs_snd[good_idxs]

    if not kwargs['uv']:
        snd['wind_dir'] = wd_obs_snd[good_idxs]
        snd['wind_spd'] = ws_obs_snd[good_idxs]

    return snd

def parse(file, src):
    snd = None
    if src.lower() == "pickle":
        snd = cPickle.load(file)
        snd = qualityControl(snd, 9999.0, 9999.0, 999.0, 999.0, 9999.0)
    elif src.lower() == "spc":
        snd = _parseSPC(file, missing=-9999.0)
        snd = qualityControl(snd, -9999.0, -9999.0, -9999.0, -9999.0, -9999.0, uv=False) 

    return snd

def _parseSPC(file, missing=None):
    track_file = False
    snd = {
        'pressure':[],
        'temperature':[],
        'dewpoint':[],
        'wind_dir':[],
        'wind_spd':[],
        'u_wind':[],
        'v_wind':[],
    }

    for line in file.read().split("\n"):
        if line.strip() == "%RAW%":
            track_file = True
        elif line.strip() == "%END%":
            track_file = False
        elif track_file:
            level_values = [ v.strip() for v in line.split(',') ]

            wdir = float(level_values[4])
            wspd = float(level_values[5])

            u = -wspd * np.sin(wdir * np.pi / 180)
            v = -wspd * np.cos(wdir * np.pi / 180)

            if missing is not None:
                pres = float(level_values[0])
                temp = float(level_values[2])
                dewp = float(level_values[3])

                if pres == missing: snd['pressure'].append(np.nan)
                else:               snd['pressure'].append(pres)

                if temp == missing: snd['temperature'].append(np.nan)
                else:               snd['temperature'].append(temp)

                if dewp == missing: snd['dewpoint'].append(np.nan)
                else:               snd['dewpoint'].append(dewp)

                if wdir == missing or wspd == missing:
                    snd['u_wind'].append(np.nan)
                    snd['v_wind'].append(np.nan)
                    snd['wind_dir'].append(np.nan)
                    snd['wind_spd'].append(np.nan)
                else:
                    snd['u_wind'].append(u)
                    snd['v_wind'].append(v)
                    snd['wind_dir'].append(wdir)
                    snd['wind_spd'].append(wspd)
            else:
                snd['pressure'].append(float(level_values[0]))
                snd['temperature'].append(float(level_values[2]))
                snd['dewpoint'].append(float(level_values[3]))
                snd['wind_dir'].append(wdir)
                snd['wind_spd'].append(wspd)
                snd['u_wind'].append(u)
                snd['v_wind'].append(v)

    for key in snd.keys():
        snd[key] = np.array(snd[key])

    return snd
