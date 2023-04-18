import csv
import matplotlib.pyplot as plt
import math
from scipy.interpolate import make_interp_spline

# Asking for delta!!!
delta = float(input("Delta: "))
conv = float(input("Conversion of Voltage : "))

drift = input("Do you want to resolve drift? (y/n) ")
sloping = input("Do you want to resolve sloping? (y/n) ")

# opening CSV file
with open("/Users/vedantaryan/Downloads/test_data_45 - Sheet1.csv", 'r') as file:
    csvreader = csv.reader(file)

    # Initializing empty arrays.
    # data=entire csv in one row.
    # h=x axis (external field)
    # i = y axis (some unit)

    data = []
    H = []
    H_corrected = []
    I = []
    phi = []
    phi_closed = []
    phi_corrected = []

    # turning csv file into a single list. removing first untitled element. replace #ev with third element
    for row in csvreader:
        data.append(row[0])
    data.remove('Untitled')
    data[1] = data[3]
    # print(data)

    # filtering huge list into sublists of h and i
    for i in range(len(data)):
        if i % 2 == 0:
            H.append(float(data[i]))
        else:
            I.append(float(data[i]))

    # print(H)
    # print(I)

    I_initial = sum(I) / len(I)

    # Converting h into real h????
    for h in H:
        hNew = h * conv
        H_corrected.append(hNew)

    # Converting current into kerr angle
    for i in I:
        phi_kerr = (i / I_initial - 1) * delta * math.pi / 180 / 2
        phi.append(phi_kerr)


if drift == 'Y':
        # print(phi)
        # Correcting noise/drift with linear drift cancellation
        run = 4 * max(H)
        rise = phi[len(phi) - 1] - phi[0]
        # Excel has -2 somehow
        slope = rise / run
        midpoint = H.index(max(H))

        # print(run)
        # print(rise)
        # print(slope)

        for i in range(len(phi)):
            if i <= midpoint:
                phiKerrClosed = phi[i] - (H[i] * slope + slope * run / 4)
                phi_closed.append(phiKerrClosed)
            else:
                phiKerrClosed = phi[i] - (H[i] * (-1) * slope + slope * run / 2)
                phi_closed.append(phiKerrClosed)
        # print(phi_closed)

        # Correcting correction for some reason
        centerClosed = sum(phi_closed) / len(phi_closed)
        # print(centerClosed)

        for phiClosed in phi_closed:
            phiNew = phiClosed - centerClosed
            phi_corrected.append(phiNew)

        # Finding coercivity
        for i in range(0, len(H) - 1):
            if (phi_corrected[i] < 0 and phi_corrected[i+1] > 0):
                corRHS = H_corrected[i]
            elif (phi_corrected[i] > 0 and phi_corrected[i+1] < 0):
                corLHS = H_corrected[i]
        coercivity = corRHS - corLHS
        print('Coercivity: ' + str(coercivity))

        #Finding remanence
        for i in range(0, len(H) - 1):
            if (H[i] == 0 and H[i+1] < 0):
                yIntercept = phi_corrected[i]
        remanence = 100 * (yIntercept / max(phi_corrected))
        print('Remanence: ' + str(remanence) + '%')


        # print(phi_corrected)
        # attempted smoothing
        # H_I_Spline = make_interp_spline(H, I)
        #
        # I_ = H_I_Spline(X_)

        # Plotting H against Current
        # plt.plot(H,I)
        # plt.title("H vs I without correction")
        # plt.xlabel("H")
        # plt.ylabel("I")
        # plt.show(H,I)

        # Plotting H against Kerr Angle without correction
        # plt.plot(H, phi)
        # plt.title("H vs Kerr Angle without correction")
        # plt.xlabel("H")
        # plt.ylabel("Kerr Angle")
        # plt.axvline(x=0, c='black')
        # plt.axhline(y=0, c='black')
        # plt.show()

        # Plotting H against Kerr with Partial Correction
        # plt.plot(H, phi_closed)
        # plt.title("H vs Kerr Angle Closed")
        # plt.xlabel("H")
        # plt.ylabel("Kerr Angle")
        # plt.axvline(x=0, c='black')
        # plt.axhline(y=0, c='black')
        # plt.show()

        plt.plot(H_corrected, phi_corrected)
        plt.title("H vs Kerr Angle")
        plt.xlabel("H")
        plt.ylabel("Kerr Angle")
        plt.axvline(x=0, c='black')
        plt.axhline(y=0, c='black')
        plt.show()



if sloping == 'Y':
    # opening CSV file
    with open("/Users/vedantaryan/Downloads/test_data_45 - Sheet1.csv", 'r') as file:
        csvreader = csv.reader(file)

        # Initializing empty arrays.
        # data=entire csv in one row.
        # h=x axis (external field)
        # i = y axis (some unit)

        data = []
        H = []
        H_corrected = []
        I = []
        phi = []
        phi_closed = []
        phi_corrected = []

        # turning csv file into a single list. removing first untitled element. replace #ev with third element
        for row in csvreader:
            data.append(row[0])
        data.remove('Untitled')
        data[1] = data[3]
        # print(data)

        # filtering huge list into sublists of h and i
        for i in range(len(data)):
            if i % 2 == 0:
                H.append(float(data[i]))
            else:
                I.append(float(data[i]))

        # print(H)
        # print(I)

        I_initial = sum(I) / len(I)

        # Converting h into real h????
        for h in H:
            hNew = h * conv
            H_corrected.append(hNew)

        # Converting current into kerr angle
        for i in I:
            phi_kerr = (i / I_initial - 1) * delta * math.pi / 180 / 2
            phi.append(phi_kerr)

        # print(phi)

        # Correcting noise/drift with linear drift cancellation
        run = 4 * max(H)
        rise = phi[len(phi) - 1] - phi[0]
        # Excel has -2 somehow
        slope = rise / run
        midpoint = H.index(max(H))

        # print(run)
        # print(rise)
        # print(slope)

        for i in range(len(phi)):
            if i <= midpoint:
                phiKerrClosed = phi[i] - (H[i] * slope + slope * run / 4)
                phi_closed.append(phiKerrClosed)
            else:
                phiKerrClosed = phi[i] - (H[i] * (-1) * slope + slope * run / 2)
                phi_closed.append(phiKerrClosed)
        # print(phi_closed)

        # Correcting correction for some reason
        centerClosed = sum(phi_closed) / len(phi_closed)
        # print(centerClosed)

        for phiClosed in phi_closed:
            phiNew = phiClosed - centerClosed
            phi_corrected.append(phiNew)

        # Finding coercivity
        for i in range(0, len(H) - 1):
            if (phi_corrected[i] < 0 and phi_corrected[i + 1] > 0):
                corRHS = H_corrected[i]
            elif (phi_corrected[i] > 0 and phi_corrected[i + 1] < 0):
                corLHS = H_corrected[i]
        coercivity = corRHS - corLHS
        print('Coercivity: ' + str(coercivity))

        # print(phi_corrected)
        # attempted smoothing
        # H_I_Spline = make_interp_spline(H, I)
        #
        # I_ = H_I_Spline(X_)

        # Plotting H against Current
        # plt.plot(H,I)
        # plt.title("H vs I without correction")
        # plt.xlabel("H")
        # plt.ylabel("I")
        # plt.show(H,I)

        # Plotting H against Kerr Angle without correction
        # plt.plot(H, phi)
        # plt.title("H vs Kerr Angle without correction")
        # plt.xlabel("H")
        # plt.ylabel("Kerr Angle")
        # plt.axvline(x=0, c='black')
        # plt.axhline(y=0, c='black')
        # plt.show()

        # Plotting H against Kerr with Partial Correction
        # plt.plot(H, phi_closed)
        # plt.title("H vs Kerr Angle Closed")
        # plt.xlabel("H")
        # plt.ylabel("Kerr Angle")
        # plt.axvline(x=0, c='black')
        # plt.axhline(y=0, c='black')
        # plt.show()

        plt.plot(H_corrected, phi_corrected)
        plt.title("H vs Kerr Angle")
        plt.xlabel("H")
        plt.ylabel("Kerr Angle")
        plt.axvline(x=0, c='black')
        plt.axhline(y=0, c='black')
        3
        plt.show()

# if drift == 'Y':
#     plt.plot(H_corrected, phi_corrected)
#     plt.title("H vs Kerr Angle")
#     plt.xlabel("H")
#     plt.ylabel("Kerr Angle")
#     plt.axvline(x=0, c='black')
#     plt.axhline(y=0, c='black')
#     plt.show()
# elif drift == 'Y':

# plt.plot(H_corrected, phi_corrected)
#         plt.title("H vs Kerr Angle")
#         plt.xlabel("H")
#         plt.ylabel("Kerr Angle")
#         plt.axvline(x=0, c='black')
#         plt.axhline(y=0, c='black')
#         plt.show()
