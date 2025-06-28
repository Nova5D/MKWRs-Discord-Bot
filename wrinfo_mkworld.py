#An implementation of the MKWorld WR info command using user input. Thanks to Jimmy for helping me with this.
import pandas as pd

#The below variable comes from Jimmy's WRless parts script
wr_data = pd.read_csv(
    "https://mkwrs.com/data/mkworld_wrs.csv", encoding='utf-8',
    names=['wr_id', 'player', 'date', 'track', 'time',
           'track_id', 'country', 'link', 'coins', 'shrooms',
           'vehicle', 'tire', 'is_current', 'glider', 'duration',
           'character', 'lap1', 'lap2', 'lap3', 'pre_release',
           'controls', 'lap4', 'lap5', 'lap6', 'lap7', 'cc'],
    header=None
)
wr_data = wr_data.sort_values(by=['wr_id'])

#Dictionary of track abbreviations
abbrevKey = {
  "MBC": 1,"CC":   2,"WS":   3,"DKS":  4,
  "RDH": 5,"RSGB": 6,"RWST": 7,"RAF":  8,
  "RDKP":9,"SP":   10,"RSHS":11,"RWSH":12,
  "RKTB":13,"FO":  14,"PS":  15,"RPB": 16,
  "SSS": 17,"RDDJ":18,"GBR": 19,"CCF": 20,
  "DD":  21,"BCN": 22,"DBB": 23,"RMMM":24,
  "RCM": 25,"RTF": 26,"BCT": 27,"AH":  28,
  "RMC": 29,"RR":  30
}

#Find the WR based on input
def findWR(dictID):
    targetTime = wr_data.loc[(wr_data.track_id == dictID) & (wr_data.is_current == 1)]
    return targetTime.iloc[0]

#Check if the WR is tied and store it. Currently only works for 2-way ties
def findTiedWR(dictID):
    wr1 = findWR(dictID)
    targetTime0 = wr_data.loc[(wr_data.track_id == dictID) & (wr_data.is_current == 1) & (wr_data.wr_id != wr1[0])]
    if not targetTime0.empty:
        return targetTime0.iloc[0]
    else:
        return targetTime0

#Displaying the time correctly
def createTime(wr):
    timeValueStr = str(wr[4])
    len_tVS = len(timeValueStr)

    minStr = timeValueStr[0:(len_tVS // 2)]
    msDisplay = timeValueStr[(len_tVS // 2):len_tVS]

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
def slashWR(dictID):
    wr = findWR(dictID)
    wr0 = findTiedWR(dictID)
    if wr0.empty:
        print(
            createTime(wr),"by",
            wr[1],"("+
            wr[6]+")"+
            createLink(wr)
            )
    #If the WR is tied:
    else:
        print(
            createTime(wr),"by",
            wr[1],"("+
            wr[6]+")"+
            createLink(wr),"and",
            wr0[1],"("+
            wr0[6]+")"+
            createLink(wr0)
            )

#More complex display with all the other info
#Choosing whether to write "day" or "days"
def createDuration(wr):
    if wr[14] == 1:
        return str(wr[14])+" day"
    else:
        return str(wr[14])+" days"

#Creating variables for splits first because RR, rKTB and DKS exist
def createSplits(wr):
    splits = wr[16]+" - "+wr[17]+" - "+wr[18]
    if wr[5] == 4 or wr[5] == 13 or wr[5] == 30:
        splits += " - "+wr[21]
        if wr[5] == 4 or wr[5] == 13:
            splits += " - "+wr[22]
            if wr[5] == 4:
                splits += " - "+wr[23]
    return splits

#Printing the info
def slashWI(dictID):
    wr = findWR(dictID)
    wr0 = findTiedWR(dictID)
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
                wr[10]
            )
    #If the WR is tied:
    else:
        print(
            createTime(wr),"by",
            wr[1],"("+
            wr[6]+")"+
            createLink(wr),"and",
            wr0[1],"("+
            wr0[6]+")"+
            createLink(wr0)+"\n"+
            wr[1]+":\n"+
                "   Date:",wr[2]+"\n"+
                "   Duration:",createDuration(wr)+"\n"+
                "   Splits:",createSplits(wr)+"\n"+
                "   Mushrooms:",wr[9]+"\n"+
                "   Coins:",wr[8]+"\n"+
                "   Combo:",
                    wr[15],"-",
                    wr[10]+"\n"+
            wr0[1]+":\n"+
                "   Date:",wr0[2]+"\n"+
                "   Duration:",createDuration(wr0)+"\n"+
                "   Splits:",createSplits(wr0)+"\n"+
                "   Mushrooms:",wr0[9]+"\n"+
                "   Coins:",wr0[8]+"\n"+
                "   Combo:",
                    wr0[15],"-",
                    wr0[10]
                )

#Ask for track abbreviation
def main():
    trackInput = input("Enter the track abbreviation:\n")
    trackInput = trackInput.upper()
    dictID = abbrevKey[trackInput]
    slashWR(dictID)
    slashWI(dictID)

main()
