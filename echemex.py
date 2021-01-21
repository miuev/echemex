import numpy as np

def readcv(FILE, cycle, E_ref, area):
    
    if cycle == -1:
        full = 1
    else:
        cycle = cycle - 1
        full = 0
        
    with open(FILE, "r") as f:
        for s in range(13):
            _ = f.readline()
        
        scanrate = []
        scan = f.readline().split()
        scan = np.array(scan)
        scanrate.append(float(scan[2]))
            
        for r in range(51):
            _ = f.readline()
                    
        V = []
        I = []
        counter = 0;
        
        for x in f:
            data = x.split()
            data = np.array(data)
            
            try:
                float(data[0])
                if (counter == cycle) or (full == 1):
                    V.append(float(data[2]))
                    I.append(float(data[3]))
            except:
                counter = counter + 1
                for skip in range(2):
                    _ = f.readline()
        f.close()
        counter = counter + 1
        V = np.array(V)-E_ref
        I = np.array(I)*1000/area
        
        numcyc = counter
                
        scanrate = format(float(np.array(scanrate)), '.0f')
        
    return V, I, scanrate, numcyc

def readeis(FILE, E_ref):
    # FILE - filepath to data
    # E_ref - reference electrode potential
    # Note: original .DTA files may not be encoded in a way that is compatible with this function
    #       duplicating the file into another blank .txt file and renaming .DTA fixes this issue
    check = 0
    with open(FILE, "r") as f:
        for s in range(10):
            _ = f.readline()

        time = []
        freq = []
        real = []
        imag = []
        delt = []
        volt = []
        
        for x in f:
            data = x.split()
            if check == 0:
                if data[0] == "ZCURVE":
                    _ = f.readline()
                    _ = f.readline()
                    check = 1
                else:
                    _ = 0
            try:
                float(data[0])
                if check == 1:
                    data = np.array(data)
                    time.append(float(data[1]))
                    freq.append(float(data[2]))
                    real.append(float(data[3]))
                    imag.append(float(data[4]))
                    delt.append(float(data[7]))
                    volt.append(float(data[9]))
            except:
                _ = 0
                
        f.close()
        
        time = np.array(time)
        freq = np.array(freq)
        real = np.array(real)
        imag = -np.array(imag)
        delt = -np.array(delt)*np.pi/180
        volt = np.array(volt)-E_ref
        

    return time, freq, real, imag, delt, volt

def readca(FILE, E_ref, area):
    
    time = []
    potential = []
    current = []
    counter = 0
    
    with open(FILE, "r") as f:
        
        for x in f:
            data = x.split()
            data = np.array(data)
            
            try:
                float(data[0])
                time.append(float(data[1]))
                potential.append(float(data[2]))
                current.append(float(data[3]))
            except:
                if data.shape == (0,):
                    _ = []
                elif data[0] == "CURVE":
                    for skip in range(2):
                        _ = f.readline()
                    counter = counter + 1
                    
        f.close()
        
        time = np.array(time)
        potential = np.array(potential)-E_ref
        current = np.array(current)*1000/area        
        
    return time, potential, current

def readcp(FILE, E_ref):
    
    with open(FILE, "r") as f:
        for s in range(62):
            _ = f.readline()
                    
        V = []
        I = []
        t = []
        counter = 0;
        full = 0;
        
        for x in f:
            data = x.split()
            data = np.array(data)
            
            try:
                float(data[0])
                V.append(float(data[2]))
                I.append(float(data[3]))
                t.append(float(data[1]))
            except:
                for skip in range(2):
                    _ = f.readline()
        f.close()
        V = np.array(V)-E_ref
        I = np.array(I)*10**3
        t = np.array(t)

    return t, V, I
