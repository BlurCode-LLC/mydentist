$("#id_phone_number").on("focus", function () {
    if ($(this).val() == "") {
        $(this).val("(")
    }
})
$("#id_phone_number").on("focusout", function () {
    if ($(this).val() == "(") {
        $(this).val("")
    }
})
$("#id_phone_number").on("keydown", function (e) {
    let val = $(this).val()
    if (e.keyCode == 8) {
        if (val.length == 11 || val.length == 8) {
            $(this).val(val.slice(0, val.length - 1))
        } else if (val.length == 4) {
            $(this).val(val.slice(0, val.length - 2))
        } else if (val.length == 0) {
            $(this).val("(")
        }
    } else if (e.keyCode == 46) {
        if (val.length == 0) {
            $(this).val("(")
        }
    } else if ([48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105].includes(e.keyCode)) {
        if (val.length == 3) {
            $(this).val(val + ") ")
        } else if (val.length == 8 || val.length == 11) {
            $(this).val(val + "-")
        } else if (val.length == 15) {
            $(this).val(val.slice(0, val.length - 1))
        }
    } else if ([65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 186, 187, 188, 189, 190, 191, 192, 193, 194, 219, 220, 221, 222, 223].includes(e.keyCode)) {
        $(this).val(val.slice(0, val.length - 1))
    }
})