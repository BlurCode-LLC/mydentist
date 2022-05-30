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
    if (e.keyCode == 8) {
        let val = $(this).val()
        console.log(val.length)
        if (val.length == 12 || val.length == 9) {
            $(this).val(val.slice(0, val.length - 1))
        } else if (val.length == 5) {
            $(this).val(val.slice(0, val.length - 2))
        }
    }
})
$("#id_phone_number").on("input", function () {
    let val = $(this).val()
    console.log(val.length)
    console.log(val[val.length - 1])
    if (! (val[val.length - 1] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", " "])) {
        $(this).val(val.slice(0, val.length - 1))
    }
    if (val.length == 3) {
        $(this).val(`${val}) `)
    } else if (val.length == 8 || val.length == 11) {
        $(this).val(`${val}-`)
    } else if (val.length == 15) {
        $(this).val(val.slice(0, val.length - 1))
    } else if (val.length == 0) {
        $(this).val("(")
    }
    console.log(val[val.length - 1])
})