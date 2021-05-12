import requests
import xlsxwriter #these modules are neccessary! make sure you have them

noError = False
while noError == False:   #error handling if user does not give a valid id. the request will give HTML which obviously causes a syntax error
    try:
        true = True
        false = False
        null = None
        userID = input("What is your user ID? \n")
        data = eval(requests.get("https://osu.ppy.sh/users/" + userID + "/scores/best?limit=50").content) #not using the API OAuth because I don't need to
        data2 = eval(requests.get("https://osu.ppy.sh/users/" + userID + "/scores/best?limit=50&offset=50").content) #try not to spam these requests. at risk of your own IP being blocked.
    except (TypeError, SyntaxError):
        print("Invalid ID. \n")
        continue
    else:
        noError = True
        
dataFinal = []
for each in data:                  #writes data as a series of lists in a list. enough said.
    dataFinal.append([each["beatmap"]["difficulty_rating"],
                      each["pp"],
                      each["weight"]["pp"],
                      each["weight"]["percentage"]/100,
                      each["accuracy"]])

for each in data2:                    #only 50 scores are displayed per page
    dataFinal.append([each["beatmap"]["difficulty_rating"],
                      each["pp"],
                      each["weight"]["pp"],
                      each["weight"]["percentage"]/100,
                      each["accuracy"]])

sheet = xlsxwriter.Workbook("scoreExported.xlsx")     #making a sheet to write to
worksheet = sheet.add_worksheet()

worksheet.write(0,0, "nth play")
worksheet.write(0,1, "Difficulty")
worksheet.write(0,2, "pp")
worksheet.write(0,3, "Weighted pp")
worksheet.write(0,4, "Weight")
worksheet.write(0,5, "Accuracy")

row=1
column=0
count = 0
for diff, pp, weighted, weight, acc in dataFinal: #write data to sheet
    worksheet.write(row, column, count)
    worksheet.write(row, column + 1, diff)
    worksheet.write(row, column + 2, pp)
    worksheet.write(row, column + 3, weighted)
    worksheet.write(row, column + 4, weight)
    worksheet.write(row, column + 5, acc)
    count += 1
    row += 1
sheet.close()
