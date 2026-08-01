// ==============================
// PRINT INVOICE
// ==============================

document.getElementById("printInvoice").addEventListener("click", function () {

    window.print();

});

// ==============================
// DOWNLOAD PDF
// ==============================

document.getElementById("downloadPDF").addEventListener("click", function () {

    const invoice = document.querySelector(".invoice-page");

    const options = {

        margin: 0.3,

        filename: `RoyalPalace_Invoice_${new Date().getTime()}.pdf`,

        image: {

            type: "jpeg",

            quality: 1

        },

        html2canvas: {

            scale: 2,

            useCORS: true,

            scrollY: 0

        },

        jsPDF: {

            unit: "in",

            format: "a4",

            orientation: "portrait"

        }

    };

    html2pdf()

        .set(options)

        .from(invoice)

        .save();

});

// ==============================
// PRINT DATE
// ==============================

console.log("Invoice Ready");

// ==============================
// OPTIONAL
// Smooth Scroll Top
// ==============================

window.scrollTo({

    top: 0,

    behavior: "smooth"

});