let server_host = "34.159.28.136"
let server_port = "8080"
// let server_host = "192.168.178.106"
// let server_port = "5000"

let endpoint = "sustainably-scanner.ml"
let api_key = "AbHgdhJTM3yzLKPuFBhvcYtBK8IZEYmAOwJhuAJKxbeKcIKtK3UIXzBeYhIZUYPNknT0alBF9A7JXatgT2EeGy5W012DaJxN5DdbsF1kz/VIV+SscQabm4FaDggvGHPfZjcaSf0wHSUUFCSbMApxXZwqwtnn4Y9wtdatpXYS326i8wE4YOPMO7/pLQ3y3bPn0o0BcWZ8tdN11ADYEzzZODWX9YkCBUDhtc/BIArSQALTCFpiAjFj+iUGS9CnIg4iQWP+64JQ95f/ykfXZ333CpM3pMtgeudjzq69RZcDWTcqo/L1Gse1gy9VpE6Zf2PUmrdcjID6b6rzzJifOwlC1KA1RmjGccjfGQ4Xh5/kXvpSM0eEtuSoh7I7/JHPaSCUezpg7mQfHrUConL1y1V6BI0JAhTXv8quidOfa5YXFcaAkuIDkW38wcZ/6sNNNP8im0+aJhL6gUMhq1a1cYnVrlXvTiPmsm8QY/pRg01f2izYqbiBhH0tnNvTcIoWrBUo7MSvPM3OXLfGPoAv4hJOVFcrEded9tNz8gZLXT6Eai/hk/jwM8G5mlcxgH5/8ZpZW7BMot4bx4GhneXeYqhe3bolgQUEaQ8e1I77RyqhxZl/gWF+e01Cu2lhnuEEYGTg9aNi7HDbLsYJkoMotoZXvWgNc7uhs33717oKeL4iBI6RD2nzWU5dPq/OjAKeMl6Nk2xDKI9oV9G5KS6zMtMPKWdKxDr+I9ieA0N2q4mpOOIRvzdQjKLmJmKD0PRToQMGSjwKJ2HN33ZH2bfrbOTshdW0sWIDZGcnJBznzYUcPBBBiw59TkMVhvOrE3fqJWwbPIo="

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
