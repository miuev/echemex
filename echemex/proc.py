import numpy as np

def readcv(FILE, cycle = -1, E_ref = 0, area = 1, quiet = False):
    
    # FILE    - path to .DTA cyclic voltammetry data file
    # cycle   - cycle number to return
    #           return all if -1
    # E_ref   - reference potential shift, default no shift
    # area    - electrode area, default no normalization
    # quiet   - suppress normalization notifications in output if True
    
    if cycle == -1:
        full = 1
    else:
        cycle = cycle - 1
        full = 0
        
    with open(FILE, "r") as f:
        V = []
        I = []
        check = 0
        counter = 0

        for x in f:
            data = x.split()
            if check == 0:
                if len(data) == 0:
                    _ = 0
                elif data[0] =="SCANRATE":
                    scanrate = data[2]
                elif data[0] == "CYCLES":
                    numcyc = data[2]
                elif data[0] == "CURVE1" or data[0] == "CURVE":
                    _ = f.readline()
                    _ = f.readline()
                    check = 1
                else:
                    _ = 0

            elif check == 1:
                try:
                    float(data[0])
                    if (counter == cycle) or (full == 1):
                        V.append(float(data[2]))
                        I.append(float(data[3]))
                    else:
                        _ = 0
                except:
                    _ = f.readline()
                    _ = f.readline()
                    counter += 1

        f.close()
        V = np.array(V)-E_ref
        I = np.array(I)*1000/area
        
    if not quiet:
        if area == 1:
            print("Current is not normalized, units are mA")
        elif area != 1:
            print("Current is normalized to area, units are mA/cm^2")
        if E_ref == 0:
            print("Potential is not shifted, units are V vs. your experimental reference")
        elif E_ref != 0:
            print("Potential is shifted, units are V vs. your adjusted reference")
        
        scanrate = format(float(np.array(scanrate)), '.0f')
    return V, I, scanrate, numcyc

def readlsv(FILE, E_ref = 0, area = 1, quiet = False):

    # FILE    - path to .DTA cyclic voltammetry data file
    # E_ref   - reference potential shift, default no shift
    # area    - electrode area, default no normalization
    # quiet   - suppress normalization notifications in output if True

    with open(FILE, "r") as f:
        V = []
        I = []
        check = 0
        counter = 0

        for x in f:
            data = x.split()
            if check == 0:
                if len(data) == 0:
                    _ = 0
                elif data[0] =="SCANRATE":
                    scanrate = data[2]
                elif data[0] == "CURVE1" or data[0] == "CURVE":
                    _ = f.readline()
                    _ = f.readline()
                    check = 1
                else:
                    _ = 0

            elif check == 1:
                try:
                    float(data[0])
                    V.append(float(data[2]))
                    I.append(float(data[3]))
                except:
                    _ = f.readline()
                    _ = f.readline()
                    counter += 1

        f.close()
        V = np.array(V)-E_ref
        I = np.array(I)*1000/area

        if not quiet:
            if area == 1:
                print("Current is not normalized, units are mA")
            elif area != 1:
                print("Current is normalized to area, units are mA/cm^2")
            if E_ref == 0:
                print("Potential is not shifted, units are V vs. your experimental reference")
            elif E_ref != 0:
                print("Potential is shifted, units are V vs. your adjusted reference")

        scanrate = format(float(np.array(scanrate)), '.0f')
    return V, I, scanrate

def readswv(FILE, E_ref = 0, area = 1, quiet = False):
    
    # FILE    - path to .DTA cyclic voltammetry data file
    # E_ref   - reference potential shift, default no shift
    # area    - electrode area, default no normalization
    # quiet   - suppress normalization notifications in output if True

    with open(FILE, "r") as f:
        V_fwd = []
        V_rev = []
        V_step = []
        I_fwd = []
        I_rev = []
        I_diff = []
        check = 0

        for x in f:
            data = x.split()
            if check == 0:
                if len(data) == 0:
                    _ = 0
                elif data[0] == "CURVE1" or data[0] == "CURVE":
                    _ = f.readline()
                    _ = f.readline()
                    check = 1
                else:
                    _ = 0

            elif check == 1:
                try:
                    float(data[0])
                    V_fwd.append(float(data[2]))
                    V_rev.append(float(data[3]))
                    V_step.append(float(data[4]))
                    I_fwd.append(float(data[5]))
                    I_rev.append(float(data[6]))
                    I_diff.append(float(data[7]))
                except:
                    _ = f.readline()
                    _ = f.readline()

        f.close()
        V_fwd = np.array(V_fwd)-E_ref
        V_rev = np.array(V_rev)-E_ref
        V_step = np.array(V_step)-E_ref
        I_fwd = np.array(I_fwd)*1000/area
        I_rev = np.array(I_rev)*1000/area
        I_diff = np.array(I_diff)*1000/area

        if not quiet:
            if area == 1:
                print("Current is not normalized, units are mA")
            elif area != 1:
                print("Current is normalized to area, units are mA/cm^2")
            if E_ref == 0:
                print("Potential is not shifted, units are V vs. your experimental reference")
            elif E_ref != 0:
                print("Potential is shifted, units are V vs. your adjusted reference")

    return V_fwd, V_rev, V_step, I_fwd, I_rev, I_diff

def readeis(FILE, E_ref = 0):
    
    # FILE    - path to .DTA EIS data file
    # E_ref   - reference potential shift, default no shift
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
    
    if not quiet:
        if E_ref == 0:
            print("Potential is not shifted, units are V vs. your experimental reference")
        elif E_ref != 0:
            print("Potential is shifted, units are V vs. your adjusted reference")
    
    return time, freq, real, imag, delt, volt

def randcirc(w,sigma,Rct,Ro,Cd):
    
    # used for fitting EIS data
    # scipy.optimize.curvefit can match this function to the raw data
    # given starting guesses sigma, Rct, Ro, and Cd
    
    Zf  = Rct + (sigma/np.sqrt(w))
    Zre = Ro + Zf/(1+(Zf**2)*(w**2)*(Cd**2))
    return Zre

def readca(FILE, E_ref = 0, area = 1, quiet = False):
    
    # FILE    - path to .DTA cyclic voltammetry file
    # E_ref   - reference potential shift, default no shift
    # area    - electrode area, default no normalization
    # quiet   - suppress normalization notifications in output if True
    
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
        
    if not quiet:
        if area == 1:
            print("Current is not normalized, units are mA")
        elif area != 1:
            print("Current is normalized to area, units are mA/cm^2")
        if E_ref == 0:
            print("Potential is not shifted, units are V vs. your experimental reference")
        elif E_ref != 0:
            print("Potential is shifted, units are V vs. your adjusted reference")        

    return time, potential, current

def readcp(FILE, E_ref = 0, quiet = False):
    
    # FILE    - path to .DTA chronopotentiometry data file
    # E_ref   - reference potential shift, default no shift
    # quiet   - suppress normalization notifications in output if True
    
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
    
    if not quiet:
        print("Current is not normalized, units are mA")
        if E_ref == 0:
            print("Potential is not shifted, units are V vs. your experimental reference")
        elif E_ref != 0:
            print("Potential is shifted, units are V vs. your adjusted reference")
    
    return t, V, I

def getocp(FILE):
    
    # FILE    - path to .DTA cyclic voltammetry data file
    
    with open(FILE, "r") as f:
        t = []
        V = []
        check = 0
        counter = 0

        for x in f:
            data = x.split()
            if check == 0:
                if len(data) == 0:
                    _ = 0
                elif data[0] == "CURVE1" or data[0] == "CURVE":
                    _ = f.readline()
                    _ = f.readline()
                    check = 1
                else:
                    _ = 0

            elif check == 1:
                float(data[0])
                t.append(float(data[1]))
                V.append(float(data[2]))
                    
        f.close()
        
        t = np.array(t)
        V = np.array(V)
        
        average = np.mean(V[-20:])
    return t, V, average

def readgitt(FILE, E_ref = 0, area = 1, quiet = False):
    
    # FILE    - path to .DTA cyclic voltammetry data file
    # E_ref   - reference potential shift, default no shift
    # area    - electrode area, default no normalization
    # quiet   - suppress normalization notifications in output if True ):
   
    with open(FILE, "r") as f:
        t = []
        V = []
        I = []
        cycle = []
        check = 0
        
        for x in f:
            data = x.split()
            if check == 0:
                if len(data) == 0:
                    _ = 0
                elif data[0] == "CURVE1" or data[0] == "CURVE":
                    _ = f.readline()
                    _ = f.readline()
                    check = 1
                else:
                    _ = 0

            elif check == 1:
                float(data[0])
                t.append(float(data[1]))
                V.append(float(data[2]))
                I.append(float(data[3]))
                cycle.append(float(data[-1]))
                    
        f.close()
        
        t = np.array(t)
        V = np.array(V)
        I = np.array(I)
        cycle = np.array(cycle)
        
        if not quiet:
            if area == 1:
                print("Current is not normalized, units are mA")
            elif area != 1:
                print("Current is normalized, units are mA/cm2")
            if E_ref == 0:
                print("Potential is not shifted, units are V vs. your experimental reference")
            elif E_ref != 0:
                print("Potential is shifted, units are V vs. your adjusted reference")

    return t, V, I, cycle