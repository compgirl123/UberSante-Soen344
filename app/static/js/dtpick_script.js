$(document).ready(function() {
    var date = new Date();
    var today = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    var end = new Date(date.getFullYear(), date.getMonth(), date.getDate());
  
    $('#datepicker1').datepicker({
        orientation: "bottom left",
        daysOfWeekDisabled: "0,6",
        daysOfWeekHighlighted: "1,2,3,4,5",
        todayHighlight: true,
        format: "mm/dd/yyyy",        
        autoclose: true       
    }).on('changeDate', function(e) {
        var dateMon = getMonday(e.format())
        var dateTue = getTuesday(e.format())
        var dateWed = getWednesday(e.format())
        var dateThu = getThursday(e.format())
        var dateFri = getFriday(e.format())

        var fmtDateMon = (dateMon.getMonth() + 1) + '/' + dateMon.getDate() + '/' +  dateMon.getFullYear();
        var fmtDateTue = (dateTue.getMonth() + 1) + '/' + dateTue.getDate() + '/' +  dateTue.getFullYear();
        var fmtDateWed = (dateWed.getMonth() + 1) + '/' + dateWed.getDate() + '/' +  dateWed.getFullYear();
        var fmtDateThu = (dateThu.getMonth() + 1) + '/' + dateThu.getDate() + '/' +  dateThu.getFullYear();
        var fmtDateFri = (dateFri.getMonth() + 1) + '/' + dateFri.getDate() + '/' +  dateFri.getFullYear();
        /* console.log("The date chosen: " + e.format());
        console.log("Resulting weekdays: " +
        "\n- Monday: " + fmtDateMon
        + "\n- Tuesday: " + fmtDateTue
        + "\n- Wednesday: " + fmtDateWed
        + "\n- Thursday: " + fmtDateThu
        + "\n- Friday: " + fmtDateFri
        ); */

        // set the dates for each day in table header
        document.getElementById('monDate').innerHTML = fmtDateMon
        document.getElementById('tueDate').innerHTML = fmtDateTue
        document.getElementById('wedDate').innerHTML = fmtDateWed
        document.getElementById('thuDate').innerHTML = fmtDateThu
        document.getElementById('friDate').innerHTML = fmtDateFri

        var doctor_picked = str.split($('#doctor_picked').value);
        var first_name = doctor_picked[0];
        var last_name = doctor_picked[1];
        
        for (i = 0; i < cars.length; i++) { 
          checkAvailability(first_name, last_name, appointment_date, start_time, end_time, monCheck, idSuffix);
          checkAvailability(first_name, last_name, appointment_date, start_time, end_time, tueCheck, idSuffix);
          checkAvailability(first_name, last_name, appointment_date, start_time, end_time, wedCheck, idSuffix);
          checkAvailability(first_name, last_name, appointment_date, start_time, end_time, thuCheck, idSuffix);
          checkAvailability(first_name, last_name, appointment_date, start_time, end_time, friCheck, idSuffix);
        }

    });
    
    
    var n=document.getElementById('datepicker1').value;
    if (n.length < 1){
        // set the default date to today
        $("#datepicker1").datepicker("setDate", new Date());
    }
   
  });

  function checkAvailability(first_name, last_name, appointment_date, start_time, end_time, idPrefix, idSuffix) {
    $.ajax({
      type: "GET",
      url: "/availablecheck",
      data: {first_name: first_name, last_name: last_name, appointment_date: appointment_date,
        start_time: start_time, end_time: end_time
      },
      success: function(data) {
        print(data);
        if (data == true){
          $('#'+idPrefix+idSuffix).attr('disabled', true);
        }
        else {
          $('#'+idPrefix+idSuffix).attr('disabled', false);
        }
      }
    });
  }

  // functions for the different days
  function getMonday(d) {
    d = new Date(d);
    var day = d.getDay(),
        diff = d.getDate() - day + (day == 0 ? -6:1); // adjust when day is sunday
    return new Date(d.setDate(diff));
  }

  function getTuesday(d) {
    d = new Date(d);
    var day = d.getDay(),
        diff = d.getDate() - day + (day == 0 ? -6:2); // adjust when day is sunday
    return new Date(d.setDate(diff));
  }

  function getWednesday(d) {
    d = new Date(d);
    var day = d.getDay(),
        diff = d.getDate() - day + (day == 0 ? -6:3); // adjust when day is sunday
    return new Date(d.setDate(diff));
  }

  function getThursday(d) {
    d = new Date(d);
    var day = d.getDay(),
        diff = d.getDate() - day + (day == 0 ? -6:4); // adjust when day is sunday
    return new Date(d.setDate(diff));
  }

  function getFriday(d) {
    d = new Date(d);
    var day = d.getDay(),
        diff = d.getDate() - day + (day == 0 ? -6:5); // adjust when day is sunday
    return new Date(d.setDate(diff));
  }

  
