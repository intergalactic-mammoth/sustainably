
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
    ScanditSDK.configure("AfSQ2mdTRgepAolsjwu0JM8dn5ONHT255B/e169bGMSgeJjCe2N4GelXOzgfVZJNwRPMya9ogf4AQS/CTVtZiXl3+WpPVibyLUFYmZNKmo5cJGTUX1v0naNNKCoEH7xvgk1BRD4uC4ToCFhORCTEr4UVxJpGMLN0f51u/SANQaIRoM0G67PWYNSAAKjBLqN+9SerGPOziRuepui7BltH7egFVO9phP/gTV9Cw8b4tghWy2cbFoJRtlI/i1cd+QjHM5n/swNambSN8w9UKwPOvxkpwSNBFZ1r9z3mqRFkZ/jkYbTc5FONyd73oRjzF1jvvGip5D1HbB1pdD58roZ8SgPVbxSCSCnoOxVtn76Rui2oZ8WGNgfFacqjcZvBtxmtsZQb9+cnBtNMvljrxp5E+5qFxFQ61811fudRKkTqg8brbKsmZGatKyNn+Ro0s0QxgohzYvMhfYCOxl8fgcYJ1uCug0g7wqX4zhz1WcAbs2y9DIrF/mIk40TQBWxyO/Wl/ljGjgJ3htuQNicfFDm1XzVKLJabIy519Jo60+fMfU7wApNvs7X5uHU01bCuyi8Mg1kT1obAuSScHUYn9obTsnANCP6jrBCIKoDoSB+p2DefqlRKEc9PD+JkajGAaghxJNrrvZlXrN50y9vuOsJEm+iCv5Ma9xiZPsmMmIREnjYBJ+WulR/dGy5eI2TvOhDuPyhnd4gdW987RdCnoysPs2OcHfoApY2eiETCC4iUn5Lib7/+NBpWLs4rG0fVs8inWnUooQTb1yJx+EXBhkefuulH4UMiirMzZ1rU5bOeDGAMkbI+GFw3q4SXOGdQ5ZFkpQutyBBg", {
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
                console.log("Sending barcode data to server");
                fetch(`http://192.168.178.78:8080/scan/001/${code}`);

                console.log("Fetching product data from server");
                // fetch(`http://192.168.178.78:8080//image/product/${code}`).then(
                //     response => response.json()
                // ).then(
                //     data => {
                //         console.log("Product image:");
                //         console.log(data);
                //         dataDiv = document.getElementById("product-data");
                //         let img = document.createElement("product-data");
                //         img.setAttribute("class", "product-img");
                //         img.setAttribute("src", data)
                //         dataDiv.appendChild(img);
                //     }
                // )
                // .then()
                fetch(`http://192.168.178.78:8080/product/${code}`)
                .then(
                    response => response.json()
                ).then(
                    data => {
                        console.log("Product data:");
                        console.log(data);
                        dataDiv = document.getElementById("product-data");
                        for (const key in jsonToText) {
                            let par = document.createElement("p")
                            par.setAttribute("class", "product-infoline");
                            let text = jsonToText[key] + ": " + data[key];
                            let textNode = document.createTextNode(text);
                            par.appendChild(textNode);
                            dataDiv.appendChild(par);
                        }
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