#An implementation of the WR info command using user input. Thanks to Jimmy for helping me with this.
import pandas as pd

#The below variable comes from Jimmy's WRless parts script
wr_data = pd.read_csv(
    "https://mkwrs.com/data/mk8dx_wrs.csv", encoding='utf-8',
    names=['wr_id', 'player', 'date', 'track', 'time',
           'track_id', 'country', 'link', 'coins', 'shrooms',
           'vehicle', 'tire', 'is_current', 'glider', 'duration',
           'character', 'lap1', 'lap2', 'lap3', 'pre_release',
           'controls', 'lap4', 'lap5', 'lap6', 'lap7', 'cc'],
    header=None
)

#Idk if there's a better way to implement this
abbrevKey = {
  "MKS": 1,"WP":   2,"SSC":  3,"TR":   4,
  "MC":  5,"TH":   6,"TM":   7,"SGF":  8,
  "SA":  9,"DS":   10,"Ed":  11,"MW":  12,
  "CC":  13,"BDD": 14,"BC":  15,"RR":  16,
  "RMMM":17,"RMC": 18,"RCCB":19,"RTT": 20,
  "RDDD":21,"RDP3":22,"RRRY":23,"RDKJ":24,
  "RWS": 25,"RSL": 26,"RMP": 27,"RYV": 28,
  "RTTC":29,"RPPS":30,"RGV": 31,"RRRD":32,
  "DYC": 33,"DEA": 34,"DDD": 35,"DMC": 36,
  "DWGM":37,"DRR": 38,"DIIO":39,"DHC": 40,
  "DBP": 41,"DCL": 42,"DWW": 43,"DAC": 44,
  "DNBC":45,"DRIR":46,"DSBS":47,"DBB": 48,
  "BPP": 49,"BTC": 50,"BCMO":51,"BCMA":52,
  "BTB": 53,"BSR": 54,"BSG": 55,"BNH": 56,
  "BNYM":57,"BMC3":58,"BKD": 59,"BWP": 60,
  "BSS": 61,"BSL": 62,"BMG": 63,"BSHS":64,
  "BLL": 65,"BBL": 66,"BRRM":67,"BMT": 68,
  "BBB": 69,"BPG": 70,"BMM": 71,"BRR7":72,
  "BAD": 73,"BRP": 74,"BDKS":75,"BYI": 76,
  "BBR": 77,"BMC": 78,"BWS": 79,"BSSY":80,
  "BATD":81,"BDC": 82,"BMH": 83,"BSCS":84,
  "BLAL":85,"BSW": 86,"BKC": 87,"BVV": 88,
  "BRA": 89,"BDKM":90,"BDCT":91,"BPPC":92,
  "BMD": 93,"BRIW":94,"BBC3":95,"BRRW":96
}

#Find the WR based on input
def findWR(dictID, ccInput):
    targetTime = wr_data.loc[(wr_data.track_id == dictID) & (wr_data.cc == ccInput) & (wr_data.is_current == 1)]
    return targetTime.iloc[0]

#Check if the WR is tied and store it. Currently only works for 2-way ties
def findTiedWR(dictID, ccInput):
    wr1 = findWR(dictID, ccInput)
    targetTime0 = wr_data.loc[(wr_data.track_id == dictID) & (wr_data.cc == ccInput) & (wr_data.is_current == 1) & (wr_data.wr_id != wr1[0])]
    if not targetTime0.empty:
        return targetTime0.iloc[0]
    else:
        return targetTime0

#Displaying the time correctly
def createTime(wr):
    timeValueStr = str(wr[4])

    if len(timeValueStr) == 5:
        minStr = timeValueStr[0:2]
        msDisplay = timeValueStr[2:5]
    elif len(timeValueStr) == 6:
        minStr = timeValueStr[0:3]
        msDisplay = timeValueStr[3:6]
    
    minInt = int(minStr)
    minDivInt = minInt // 60
    secModInt = minInt % 60
    if secModInt < 10:
        secDisplay = "0" + str(secModInt)
    else:
        secDisplay = str(secModInt)

    return str(minDivInt) + ":" + secDisplay + "." + msDisplay

#Handling video link (in case there isn't one)
def createLink(wr):
    if pd.isna(wr[7]):
        return ""
    else:
        return " - "+wr[7]

#Simple display of time, player, country and link
def slashWR(dictID, ccInput):
    wr = findWR(dictID, ccInput)
    wr0 = findTiedWR(dictID, ccInput)
    if wr0.empty:
        print(
            createTime(wr),"by",
            wr[1],"("+
            wr[6]+")",
            createLink(wr)
            )
    #If the WR is tied:
    else:
        print(
            createTime(wr0),"by",
            wr0[1],"("+
            wr0[6]+")"+
            createLink(wr0),"and",
            wr[1],"("+
            wr[6]+")"+
            createLink(wr)
            )


#More complex display with all the other info
#Choosing whether to write "day" or "days"
def createDuration(wr):
    if wr[14] == 1:
        return str(wr[14])+" day"
    else:
        return str(wr[14])+" days"

#Creating variables for splits first because dBP exists for some reason
def createSplits(wr):
    splits = wr[16]+" - "+wr[17]+" - "+wr[18]
    if wr[5] == 41:
        splits += " - "+wr[21]+" - "+wr[22]+" - "+wr[23]+" - "+wr[24]
    return splits

#Determining controls status
def createControls(wr):
    ctrlStatus = wr[20]
    if ctrlStatus == 2:
        return "Hybrid Controls used"
    elif ctrlStatus == 1:
        return "Tilt Controls predominantly used"
    else:
        return "None"

#Printing the info
def slashWI(dictID, ccInput):
    wr = findWR(dictID, ccInput)
    wr0 = findTiedWR(dictID, ccInput)
    if wr0.empty:
        print(
            createTime(wr),"by",
            wr[1],"("+
            wr[6]+")"+
            createLink(wr)+"\n"+
            "Date:",wr[2]+"\n"+
            "Duration:",createDuration(wr)+"\n"+
            "Splits:",createSplits(wr)+"\n"+
            "Mushrooms:",wr[9]+"\n"+
            "Coins:",wr[8]+"\n"+
            "Combo:",
                wr[15],"-",
                wr[10],"-",
                wr[11],"-",
                wr[13]+"\n"+
            "Motion:",createControls(wr)
            )
    #If the WR is tied:
    else:
        print(
            createTime(wr0),"by",
            wr0[1],"("+
            wr0[6]+")"+
            createLink(wr0),"and",
            wr[1],"("+
            wr[6]+")"+
            createLink(wr)+"\n"+
            wr0[1]+":\n"+
                "   Date:",wr0[2]+"\n"+
                "   Duration:",createDuration(wr0)+"\n"+
                "   Splits:",createSplits(wr0)+"\n"+
                "   Mushrooms:",wr0[9]+"\n"+
                "   Coins:",wr0[8]+"\n"+
                "   Combo:",
                    wr0[15],"-",
                    wr0[10],"-",
                    wr0[11],"-",
                    wr0[13]+"\n"+
                "   Motion:",createControls(wr0)+"\n"+
            wr[1]+":\n"+
                "   Date:",wr[2]+"\n"+
                "   Duration:",createDuration(wr)+"\n"+
                "   Splits:",createSplits(wr)+"\n"+
                "   Mushrooms:",wr[9]+"\n"+
                "   Coins:",wr[8]+"\n"+
                "   Combo:",
                    wr[15],"-",
                    wr[10],"-",
                    wr[11],"-",
                    wr[13]+"\n"+
                "   Motion:",createControls(wr)
                )

#Ask for track abbreviation and speed
def main():
    trackInput = input("Enter the track abbreviation:\n")
    trackInput = trackInput.upper()
    dictID = abbrevKey[trackInput]
    ccInput = int(input("Enter the speed:\n"))
    slashWR(dictID, ccInput)
    slashWI(dictID, ccInput)

main()
