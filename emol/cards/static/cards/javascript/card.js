function printCard() {
    var buttons = document.getElementById('buttons');

    buttons.style.display = 'none';
    window.print();
    buttons.style.display = 'block';
}

function downloadPDF() {
    html2canvas(document.getElementById('card')).then(function (canvas) {
        var pdf = new jspdf.jsPDF('l', 'px', [canvas.width + 10, canvas.height + 10]);
        pdf.addImage(canvas.toDataURL('image/jpeg'), 'JPEG', 5, 5, canvas.width, canvas.height);
        pdf.save('ealdormere_auth_card.pdf');
    });
}

document.addEventListener('DOMContentLoaded', function () {
    var printButton = document.getElementById('print-button');
    printButton.addEventListener('click', function () {
        printCard();
    });

    var pdfButton = document.getElementById('pdf-button');
    pdfButton.addEventListener('click', function () {
        downloadPDF();
    });
});