function updateLeaveData(jsonInput, option) {
    var spreadsheetId = "1z5NJ_fepnPul1QNWYRJpQ9cU_Btgz968QRg_OkXqkkw";
    var recordSheetName = "Total";
    
    var spreadsheet = SpreadsheetApp.openById(spreadsheetId);
    var recordSheet = spreadsheet.getSheetByName(recordSheetName);
    
    if (recordSheet) {
      var leaveData = JSON.parse(jsonInput);
      var memberColumn = recordSheet.getRange("A4:A11").getValues();
    
      var monthRange = recordSheet.getRange("A2:E2");
      monthRange.merge();
      monthRange.setValue(`Leave Tracker -${option == "current" ? getCurrentMonth() : ""} ${getCurrentYear()}`);
      
      for (var i = 0; i < leaveData.length; i++) {
        var member = leaveData[i].Member;
        var leaves = leaveData[i].Leaves;
        
        var rowIndex = getMemberRowIndex(member, memberColumn);
        if (rowIndex !== -1) {
          var leaveRange = recordSheet.getRange(rowIndex, 2, 1, 4);
          var leaveValues = [leaves.AM, leaves.PM, leaves.AA, leaves.SL];
          
          leaveRange.setValues([leaveValues]);
        }
      }
    }
  }
  
  function getMemberRowIndex(member, memberColumn) {
    for (var i = 0; i < memberColumn.length; i++) {
      if (memberColumn[i][0] === member) {
        return i + 4; // Adding 4 to account for the offset of A4
      }
    }
    return -1; // Member not found
  }
  
  function getCurrentMonth() {
    return Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "MMMM");
  }
  
  function getCurrentYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    return currentYear;
  }
  
  function calculateCurrentMonth() {
    var spreadsheetId = "1z5NJ_fepnPul1QNWYRJpQ9cU_Btgz968QRg_OkXqkkw";
    var currentMonth = getCurrentMonth();
    
    var spreadsheet = SpreadsheetApp.openById(spreadsheetId);
    var sheet = spreadsheet.getSheetByName(currentMonth);
    
    if (sheet) {
      var startRow = 6;
      var endRow = 13;
      var startColumn = 3; 
      var endColumn = 33; 
      var memberNames = sheet.getRange(startRow, 2, endRow - startRow + 1, 1).getValues();
      
      var leaveData = [];
      
      for (var i = 0; i < memberNames.length; i++) {
        var member = memberNames[i][0];
        var leaves = { AM: 0, PM: 0, AA: 0, SL: 0 };
        
        for (var column = startColumn; column <= endColumn; column++) {
          var cellValue = sheet.getRange(startRow + i, column).getValue();
          
          if (cellValue === "AM") {
            leaves.AM++;
          } else if (cellValue === "PM") {
            leaves.PM++;
          } else if (cellValue === "AA") {
            leaves.AA++;
          } else if (cellValue === "SL") {
            leaves.SL++;
          }
        }
        
        var memberLeaves = {
          Member: member,
          Leaves: leaves
        };
        
        leaveData.push(memberLeaves);
      }
      
      var jsonData = JSON.stringify(leaveData);
      updateLeaveData(jsonData, "current");
    }
  }
  
  
  function bizSalesGetMemberRowIndex(member, memberColumn) {
    for (var i = 0; i < memberColumn.length; i++) {
      if (memberColumn[i][0] === member) {
        return i + 4; // Adding 4 to account for the offset of A4
      }
    }
    return -1; // Member not found
  }
  
  function bizSalesGetCurrentMonth() {
    return Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "MMMM");
  }
  
  function bizSalesGetCurrentYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    return currentYear;
  }
  
  
  function doGet(e) {
      var spreadsheetId = "1z5NJ_fepnPul1QNWYRJpQ9cU_Btgz968QRg_OkXqkkw";
      var ignoreList = ["Reference", "Total"];
      var ignoreMemberNames = ["Riddhi", "Kartik", "Ainnur"]
      
      var spreadsheet = SpreadsheetApp.openById(spreadsheetId);
      var sheets = spreadsheet.getSheets();
      var leaveData = [];
  
      for (var i = 0; i < sheets.length; i++) {
        var sheetName = sheets[i].getName();
        
        if (!ignoreList.includes(sheetName)) {
          var currentMonth = sheetName;
          var sheet = spreadsheet.getSheetByName(currentMonth);
          
          if (sheet) {
            var startRow = 6;
            var endRow = 20;
            var startColumn = 3; 
            var endColumn = 33; 
            var memberNames = sheet.getRange(startRow, 2, endRow - startRow + 1, 1).getValues();
        
            
        
            for (var j = 0; j < memberNames.length; j++) {
              var member = memberNames[j][0];
              var leaves = { AM: 0, PM: 0, AA: 0, SL: 0 };
          
              for (var column = startColumn; column <= endColumn; column++) {
                var cellValue = sheet.getRange(startRow + j, column).getValue();
            
                if (cellValue === "AM") {
                  leaves.AM++;
                } else if (cellValue === "PM") {
                  leaves.PM++;
                } else if (cellValue === "AA") {
                  leaves.AA++;
                } else if (cellValue === "SL") {
                  leaves.SL++;
                }
              }
          
              var memberLeaves = {
                Member: member,
                Leaves: leaves
              };

                if(!ignoreMemberNames.includes(member)){
                    leaveData.push(memberLeaves);
                }
            }
          }
        }
      }
  
  
      var mergedData = leaveData.reduce(function(acc, curr) {
      var member = curr.Member.trim();
      var leaves = curr.Leaves;
  
      if(member !== ""){
        if (!acc[member]) {
          acc[member] = leaves;
        } else {
          acc[member].AM += leaves.AM;
          acc[member].PM += leaves.PM;
          acc[member].AA += leaves.AA;
          acc[member].SL += leaves.SL;
        }
      }
      return acc;
      }, {});
  
      var mergedArray = Object.keys(mergedData).map(function(member) {
        return { Member: member, Leaves: mergedData[member] };
      });
  
      var mergedJson = JSON.stringify(mergedArray);
      let techResponse = mergedJson
  
  
      var spreadsheetId = "1dbajsK7T3QBbSuyow5uGKT8E8t_c6OoBd7VhiB4N-Nk";
      var ignoreList = ["Reference", "Total"];
      
      var spreadsheet = SpreadsheetApp.openById(spreadsheetId);
      var sheets = spreadsheet.getSheets();
      var leaveData = [];
  
      for (var i = 0; i < sheets.length; i++) {
        var sheetName = sheets[i].getName();
        
        if (!ignoreList.includes(sheetName)) {
          var currentMonth = sheetName;
          var sheet = spreadsheet.getSheetByName(currentMonth);
          
          if (sheet) {
            var startRow = 6;
            var endRow = 20;
            var startColumn = 3; 
            var endColumn = 33; 
            var memberNames = sheet.getRange(startRow, 2, endRow - startRow + 1, 1).getValues();
        
            
        
            for (var j = 0; j < memberNames.length; j++) {
              var member = memberNames[j][0];
              var leaves = { AM: 0, PM: 0, AA: 0, SL: 0 };
          
              for (var column = startColumn; column <= endColumn; column++) {
                var cellValue = sheet.getRange(startRow + j, column).getValue();
            
                if (cellValue === "AM") {
                  leaves.AM++;
                } else if (cellValue === "PM") {
                  leaves.PM++;
                } else if (cellValue === "AA") {
                  leaves.AA++;
                } else if (cellValue === "SL") {
                  leaves.SL++;
                }
              }
          
              var memberLeaves = {
                Member: member,
                Leaves: leaves
              };
          
              leaveData.push(memberLeaves);
            }
        
            
          }
        }
      }
  
  
      var mergedData = leaveData.reduce(function(acc, curr) {
      var member = curr.Member.trim();
      var leaves = curr.Leaves;
  
      if(member !== ""){
        if (!acc[member]) {
          acc[member] = leaves;
        } else {
          acc[member].AM += leaves.AM;
          acc[member].PM += leaves.PM;
          acc[member].AA += leaves.AA;
          acc[member].SL += leaves.SL;
        }
      }
  
      return acc;
      }, {});
  
      var mergedArray = Object.keys(mergedData).map(function(member) {
        return { Member: member, Leaves: mergedData[member] };
      });
  
      var mergedJson = JSON.stringify(mergedArray);
      let bizSalesResponse = mergedJson
      
  
      const responseData = {
        "tech": JSON.parse(techResponse),
        "bizsales": JSON.parse(bizSalesResponse)
      };
  
      console.log(JSON.stringify(responseData));
      
      return ContentService.createTextOutput(JSON.stringify(responseData));
  }
  