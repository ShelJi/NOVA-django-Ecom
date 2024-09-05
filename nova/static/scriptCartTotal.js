let dprice = document.getElementsByClassName("discountprices");
let tprice = document.getElementsByClassName("totalprices");
let scount = document.getElementsByClassName("stockcounts");
let ctotal = document.getElementsByClassName("counttotal")[0];
let grandtotal = document.getElementsByClassName("grandtotal")[0];

let grandtotalval = 0;
let ctotalval = 0;

for (let d = 0; d < dprice.length; d++) {
    let dval = parseInt(dprice[d].innerText, 10);
    let sval = parseInt(scount[d].value, 10);

    let total = dval * sval;

    ctotalval += sval;
    grandtotalval += total;

    tprice[d].innerText = total;
}

ctotal.innerText = ctotalval;
grandtotal.innerText = grandtotalval;