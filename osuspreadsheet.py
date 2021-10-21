# hello_psg.py

import PySimpleGUI as sg
import requests
import xlsxwriter

layout = [[sg.Text("Please give your User ID")], 
          [sg.Input(key="_IN_")], 
          [sg.Button("Continue")]]

# Create the window
window = sg.Window("osu-spreadsheet", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Continue": 
        noError = False
        while noError == False:
            try:
                true = True
                false = False
                null = None
                userID = values["_IN_"]
                data = eval(requests.get("https://osu.ppy.sh/users/" + userID + "/scores/best?limit=50").content) #not using the API OAuth because I don't need to)
                data2 = eval(requests.get("https://osu.ppy.sh/users/" + userID + "/scores/best?limit=50&offset=50").content) #try not to spam these requests. at risk of your own IP being blocked.
            except (TypeError, SyntaxError):
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
        break
    if event == sg.WIN_CLOSED:
        break

window.close()
