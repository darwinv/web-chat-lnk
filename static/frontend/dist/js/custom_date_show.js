function dateTextCustom(p_datetime, p_tz) {
    p_datetime.utcOffset(p_tz);
    //console.log(p_datetime.format('YYYY-MM-DD HH:mm:ss'));
    var today12am = moment().startOf('day');
    var yesterday12am = moment().startOf('day').add(-1, 'day');
    var custom_text = "";
    //     console.log(moment(aux_1).isBetween(aux_2, aux_3, null, '[]'));
    if (p_datetime.isBetween(yesterday12am, today12am)) {
        if(window.navigator.language !="en-US"){
            custom_text = "Ayer";
        }else {
            custom_text = "Yesterday";
        }
    }
    else if (p_datetime.isBefore(yesterday12am)) {
        custom_text = moment(p_datetime).format('DD/MM/YY');
    }
    else {
        custom_text = moment(p_datetime).format('LT');
    }
    return custom_text;
}