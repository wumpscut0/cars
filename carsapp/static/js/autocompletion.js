function createOption(dom, value) {
    const option = document.createElement("option");
    option.value = value;
    dom.append(option);
}


function genDataListOptions(dataListDom, dataArr, patternStr=undefined) {
    if (patternStr) {
        dataArr.forEach(element => {
            if (element.toLowerCase().startsWith(patternStr.toLowerCase())) {
                createOption(dataListDom, element);
            };
        });
    } else {
        dataArr.forEach(element => {
            createOption(dataListDom, element);
        });
    };
};


document.addEventListener("DOMContentLoaded", () => {
    const makes = latinData.map(carData => carData.brand);
    const makeInput = document.getElementById("id_make");
    makeInput.setAttribute("list", "makes");
    makeInput.setAttribute("autocomplete", "off")
    const makesDataList = document.createElement("datalist");
    makesDataList.id = "makes";
    makeInput.insertAdjacentElement("afterend", makesDataList);
    
    genDataListOptions(makesDataList, makes);

    const models = new Set(latinData.map(carData => carData.models).flat());
    const modelInput = document.getElementById("id_model");
    modelInput.setAttribute("list", "models");
    modelInput.setAttribute("autocomplete", "off")
    const modelsDataList = document.createElement("datalist");
    modelsDataList.id = "models";
    modelInput.insertAdjacentElement("afterend", modelsDataList);

    function modelAutoComplete() {
        modelsDataList.innerHTML = "";
        const carDataByBrand = latinData.find(carData => carData.brand === makeInput.value);
        if (carDataByBrand) {
            genDataListOptions(modelsDataList, carDataByBrand.models);
        } else {
            if (modelInput.value) {
                genDataListOptions(modelsDataList, models, modelInput.value);
            };
        }; 
    };

    modelInput.addEventListener("input", () => {
        modelAutoComplete();
    });

    modelInput.addEventListener("click", () => {
        modelAutoComplete();
    });
});