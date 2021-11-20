let server_host = "34.159.28.136"
let server_port = "8080"
// let server_host = "192.168.178.106"
// let server_port = "5000"

let endpoint = "sustainably-scanner.ml"
let api_key = "AX2gjgRTJWjbGGvClhJtWGY1ZvliBkLaEHNa671S6h7KblIqpl+FbpFy89TqRCzNAU6dBh9Qj2T4bCD6QVrBOT9ikDhQLmJGs3xohUNmLrD5IaRaIE7uerpngUHNKbz6PH3lJhhIBSjhdSzYemA0lidCHDOzbdKj0hGrNw85f2BKD/rxgBqgxC8nYOnA+ZsZ4VQYFa3m5j8D/c3Fn7D6iObZzlCJrd78yAxlWLycP5c7tR+0TFiBKHIpwS+UFtirecMh8vOvF/vz1Nkn2alaxpXKQ8vYkqsj8693k4CeezSNDyTBEc6UCsl6XqkFaBX7Egm0Exo/YSphdVx8ma6HlsJmL9v3GzLfBIzI752sCLuf4Rsk9vqtzvjsB1YYExNFXb7E/pv6mRaxsWmnsobjmLg19Aouf2KeY381ty+SLHbmSHJHUafRPuDFTlL0VEGcVke8/VJTI0RgEsn1TfZO4QbuhMOX7/blRKfALtGEg2ZlPOcL/w6Bkzi0zqTix3uXY4L8Tmlho3S3GdHcq1h1DypVsA3Du9rnR26hpgu0gahEqYz4fuklPTcFetY5mNV4YOjE1qFHX4YGpul8NkaGjDpyxYeiy4wM0/Gv++YoQfZHX8t9t2elfq5CRQfkp22LRtvPcPZ3bY+zHz/++LyiF25z83dZmYVT70yiXLDhPytXxk93IqWiAbR0LZuZhJbMPUJUThhdkpdTVmPUk+USdbU3w6PG5/G0TC/i+6w5CZ6X5TRAq7XUetxjLb5SlWNW9BRJj77YmOJqO1c1qw+0uuuds1nCZ+moWtEA8NTnPwW968Itf2IMa5MAezQ0JyfUPXMboerWPXBOn5KvwHwo/kJxBdw52evZCQ=="

let jsonToText = {
    "Name": "Name",
    "Packaging_Type": "Packaging",
    "Country_Origin": "Origin Country",
    "Critical Ingredients": "Harmful",
    "Certifications": "Certifications",
    "Notes": "Additional info",
}

function injectData() {
    console.log("Injecting product data to div")
    dataDiv = document.getElementById("product-data");
    dataDiv.append(productData);
}

function scanner() {
    ScanditSDK.configure(api_key, {
        engineLocation: "https://cdn.jsdelivr.net/npm/scandit-sdk@5.x/build/",
        preloadEngineLibrary: boolean = false,
        preloadCameras: boolean = false
    }).then(() => {
        ScanditSDK.BarcodePicker.create(document.getElementById("scandit-barcode-picker"), {
            playSoundOnScan: false,
            vibrateOnScan: true,
            scanSettings: new ScanditSDK.ScanSettings({
                enabledSymbologies: ["ean8", "ean13", "upca", "upce"],
                codeDuplicateFilter: 2000,
            }),
        }).then(function (barcodePicker) {
            barcodePicker.on("scan", (scanResult) => {
                console.log(scanResult);
                console.log(scanResult.barcodes[0].data);

                code = scanResult.barcodes[0].data;

                // send scanned item to backen
                console.log("Sending barcode data to server");
                fetch(`http://${endpoint}/scan/001/${code}`);

                // get product photo
                console.log("Fetching product data from server");
                fetch(`http://${endpoint}/image/product/${code}`)
                  .then(res => res.blob())
                  .then(
                    blob => {
                      let imgUrl = URL.createObjectURL(blob);
                      let imgElement = document.getElementById("product-img");
                      imgElement.setAttribute("style", "");
                      imgElement.setAttribute("src", imgUrl)
                    }
                )

                // get product data
                fetch(`http://192.168.178.78:8080/product/${code}`)
                .then(
                    response => response.json()
                ).then(
                    data => {
                        console.log("Product data:");
                        console.log(data);

                        let productTitleElement = document.getElementById("product-title");
                        productTitleElement.innerHTML = data['Name'];

                        let productBrandElement = document.getElementById("product-brand");
                        productBrandElement.innerHTML = data['brand']['Name'];

                        let productSustScoreElement = document.getElementById("product-score");
                        productSustScoreElement.innerHTML = data['Sustainably_Score'];

                        let productCountryElement = document.getElementById("product-country");
                        productCountryElement.innerHTML = data['Country_Origin'];

                        let productCarbonFootElement = document.getElementById("product-co2");
                        productCarbonFootElement.innerHTML = data['CO2_Eqiv'];

                        let productPackageRecyclability = document.getElementById("product-recyclability");
                        productPackageRecyclability.innerHTML = data['Packaging_Score'];

                        let productDataParent = document.getElementById("product-data");
                        productDataParent.setAttribute("style", "");
                    }
                )
            });
        });
    })
}

function scannerApp() {

    if (window.location.href.split('/').pop().split('.')[0] == "scanner") {
        console.log("Initializing scanner app...")
        scanner()
    }

}
