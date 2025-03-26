async function getItems() {
    const response = await fetch("/getitems/");
    let data = await response.json();
    return data;
};
async function getPaymentModes() {
    const response = await fetch("/getPayTypes/");
    let data = await response.json();
    return data;
};
async function getMainCategory() {
    const response = await fetch("/getMainCategory/");
    let data = await response.json();
    return data;
};
let itemData;
let ItemsDiv = document.getElementById("ItemsDiv");
let orderSection=document.getElementById('orderSection');
let selectedItemsList = []
let quantitySelected = []
let showItems = document.getElementById("showItems");
let total = 0;
let total_block = document.getElementById("total");
let totalInput = document.getElementById("TotalInput");
totalInput.value = total;
total_block.innerHTML = "Total : 0";
let itemsList = document.getElementById("SelectedItems");
let quantity = document.getElementById("Quantity");
getItems().then(data => {
    getMainCategory().then(catData => {
        let mainCategories = JSON.parse(catData);
        let mainCategoriesDict = {};
        mainCategories.forEach(element => {
            mainCategoriesDict[element] = `<div class="mainCategory">${element}</div>`;
        });
        itemData = JSON.parse(data);
        let html = "";
        let categoryWithIds = {};
        let categoryWithIdsThreeCols = {};
        itemData.name.forEach((element, count) => {
            if (itemData.item_size[count] != "None") {
                if (`${element}${itemData.category[count]}` in categoryWithIds) {
                    categoryWithIds[`${element}${itemData.category[count]}`][itemData.item_size[count]] = itemData.item_id[count];
                } else {
                    categoryWithIds[`${element}${itemData.category[count]}`] = {};
                    categoryWithIds[`${element}${itemData.category[count]}`][itemData.item_size[count]] = itemData.item_id[count];
                    categoryWithIds[`${element}${itemData.category[count]}`]['mainCategory'] = itemData.maincategory[count];
                    categoryWithIds[`${element}${itemData.category[count]}`]['name'] = element;
                }
            } else {
                if (`${itemData.maincategory[count]}` in categoryWithIdsThreeCols) {
                    categoryWithIdsThreeCols[`${itemData.maincategory[count]}`]["html"] += `<div class="threeColName">${element}</div>
                                                                                                <div>
                                                                                                    <input type="checkbox" id="${itemData.item_id[count]}">
                                                                                                </div>
                                                                                                <div>
                                                                                                    <input type="number" id="${itemData.item_id[count]}_quantity" class="quantityInput" value="1">
                                                                                                </div>`;
                } else {
                    categoryWithIdsThreeCols[`${itemData.maincategory[count]}`] = {};
                    categoryWithIdsThreeCols[`${itemData.maincategory[count]}`]["html"] = `<div class="threeCols">
                                                                                                <div class="headingBold">Items</div>
                                                                                                <div class="headingBold">Select</div>
                                                                                                <div class="headingBold">Quantity</div>
                                                                                                    <div class="threeColName">${element}</div>
                                                                                                    <div>
                                                                                                        <input type="checkbox" id="${itemData.item_id[count]}">
                                                                                                    </div>
                                                                                                    <div>
                                                                                                        <input type="number" id="${itemData.item_id[count]}_quantity" class="quantityInput" value="1">
                                                                                                    </div>`;
                    categoryWithIdsThreeCols[`${itemData.maincategory[count]}`]['name'] = element;
                }
            }
        });
        let finalCategoriesHtml = {};
        Object.keys(categoryWithIds).forEach(element => {
            if (categoryWithIds[element]["mainCategory"] in finalCategoriesHtml) {
                finalCategoriesHtml[categoryWithIds[element]["mainCategory"]] += `<div class="fiveColName">${categoryWithIds[element]["name"]}</div>
                                                        <div>
                                                            <input type="checkbox" id="${categoryWithIds[element]["Small"]}">
                                                            <input type="number" id="${categoryWithIds[element]["Small"]}_quantity_inline" class="quantityInput displaySmall" value="1">
                                                        </div>
                                                        <div class="smallQuantityDiv">
                                                            <input type="number" id="${categoryWithIds[element]["Small"]}_quantity" class="quantityInput" value="1">
                                                        </div>
                                                        <div>
                                                            <input type="checkbox" id="${categoryWithIds[element]["Medium"]}">
                                                            <input type="number" id="${categoryWithIds[element]["Medium"]}_quantity_inline" class="quantityInput displayMedium" value="1">
                                                        </div>
                                                        <div class="mediumQuantityDiv">
                                                            <input type="number" id="${categoryWithIds[element]["Medium"]}_quantity" class="quantityInput" value="1">
                                                        </div>
                                                        <div>
                                                            <input type="checkbox" id="${categoryWithIds[element]["Large"]}">
                                                            <input type="number" id="${categoryWithIds[element]["Large"]}_quantity_inline" class="quantityInput displayLarge" value="1">
                                                        </div>
                                                        <div class="largeQuantityDiv">
                                                            <input type="number" id="${categoryWithIds[element]["Large"]}_quantity" class="quantityInput" value="1">
                                                        </div>`;
            } else {
                finalCategoriesHtml[categoryWithIds[element]["mainCategory"]] = "";
                finalCategoriesHtml[categoryWithIds[element]["mainCategory"]] += `<div class="fiveCols">
                                                        <div class="headingBold">Items</div>
                                                        <div class="headingBold shortNames">Small</div>
                                                        <div class="headingBold quantityNone">Quantity</div>
                                                        <div class="headingBold shortNames">Medium</div>
                                                        <div class="headingBold quantityNone">Quantity</div>
                                                        <div class="headingBold shortNames">Large</div>
                                                        <div class="headingBold quantityNone">Quantity</div>
                                                        <div class="fiveColName">${categoryWithIds[element]["name"]}</div>
                                                        <div>
                                                            <input type="checkbox" id="${categoryWithIds[element]["Small"]}">
                                                            <input type="number" id="${categoryWithIds[element]["Small"]}_quantity_inline" class="quantityInput displaySmall" value="1">
                                                        </div>
                                                        <div class="smallQuantityDiv">
                                                            <input type="number" id="${categoryWithIds[element]["Small"]}_quantity" class="quantityInput" value="1">
                                                        </div>
                                                        <div>
                                                            <input type="checkbox" id="${categoryWithIds[element]["Medium"]}">
                                                            <input type="number" id="${categoryWithIds[element]["Medium"]}_quantity_inline" class="quantityInput displayMedium" value="1">
                                                        </div>
                                                        <div class="mediumQuantityDiv">
                                                            <input type="number" id="${categoryWithIds[element]["Medium"]}_quantity" class="quantityInput" value="1">
                                                        </div>
                                                        <div>
                                                            <input type="checkbox" id="${categoryWithIds[element]["Large"]}">
                                                            <input type="number" id="${categoryWithIds[element]["Large"]}_quantity_inline" class="quantityInput displayLarge" value="1">
                                                        </div>
                                                        <div class="largeQuantityDiv">
                                                            <input type="number" id="${categoryWithIds[element]["Large"]}_quantity" class="quantityInput" value="1">
                                                        </div>`;
            }
        });
        Object.keys(categoryWithIdsThreeCols).forEach(element => {
            categoryWithIdsThreeCols[element]["html"] += `</div>`;
            mainCategoriesDict[element] += categoryWithIdsThreeCols[element]["html"];
        });
        Object.keys(finalCategoriesHtml).forEach(element => {
            finalCategoriesHtml[element] += `</div>`;
            mainCategoriesDict[element] += finalCategoriesHtml[element];
        });
        html += ` <div id="ItemsSection" class="styled-scrollbars">`;
        Object.keys(mainCategoriesDict).forEach(element => {
            html += mainCategoriesDict[element];
        });
        html += `</div>
                <div id="AddItemsBtnContainer">
                    <button id="addSelectedItems">Add</button>
                </div>`;
        ItemsDiv.innerHTML += html;
        let shortNames = document.querySelectorAll(".shortNames");
        shortNames.forEach(element => {
            if (window.innerWidth <= 500){
                element.innerHTML = element.innerHTML[0];
            }
        });
        let addSelectedItems = document.getElementById("addSelectedItems");
        addSelectedItems.addEventListener("click", () => {
            ItemsDiv.style.display='none';
            orderSection.style.display='grid';
            let threeColsCheckBoxes = document.querySelectorAll(".threeCols > div > input[type=checkbox]");
            threeColsCheckBoxes.forEach(element => {
                if (element.checked == true){
                    let quantityId = document.getElementById(`${element.id}_quantity`);
                    let selectedItemInt = element.id;
                    if (selectedItemsList.includes(parseInt(element.id))){
                        let indexOfSelected = selectedItemsList.indexOf(parseInt(element.id));
                        quantitySelected[indexOfSelected] += parseInt(quantityId.value);
                        quantity.value = quantitySelected;
                    }else{
                        selectedItemsList.push(parseInt(element.id));
                        quantitySelected.push(parseInt(quantityId.value));
                        itemsList.value = selectedItemsList;
                        quantity.value = quantitySelected;
                    }
                    for (let i = 0; i < parseInt(quantityId.value); i++){
                        let index = itemData.item_id.indexOf(parseInt(selectedItemInt));
                        // Craeted Element SVG and Line
                        const parentDiv = document.createElement("div");
                        const nameDiv = document.createElement("div");
                        const addedItem = document.createTextNode(`${itemData.name[index]} `);
                        nameDiv.appendChild(addedItem);
                        const btnDiv = document.createElement("div");
                        const svgDiv = document.createElementNS("http://www.w3.org/2000/svg", "svg");
                        svgDiv.setAttribute("viewBox", "0 0 100 100");
                        svgDiv.setAttribute("width", "20px");
                        svgDiv.classList.add(parseInt(selectedItemInt));
                        const line1 = document.createElementNS("http://www.w3.org/2000/svg", "line");
                        line1.setAttribute("x1", "10");
                        line1.setAttribute("x2", "80");
                        line1.setAttribute("y1", "20");
                        line1.setAttribute("y2", "80");
                        line1.setAttribute("stroke-width", "10");
                        line1.setAttribute("stroke-linecap", "round");
                        line1.setAttribute("stroke", "red");
                        line1.classList.add(parseInt(selectedItemInt));
                        const line2 = document.createElementNS("http://www.w3.org/2000/svg", "line");
                        line2.setAttribute("x1", "10");
                        line2.setAttribute("x2", "80");
                        line2.setAttribute("y1", "80");
                        line2.setAttribute("y2", "20");
                        line2.setAttribute("stroke-width", "10");
                        line2.setAttribute("stroke-linecap", "round");
                        line2.setAttribute("stroke", "red");
                        line2.classList.add(parseInt(selectedItemInt));
                        svgDiv.appendChild(line1);
                        svgDiv.appendChild(line2);
                        btnDiv.appendChild(svgDiv);
                        parentDiv.appendChild(nameDiv);
                        parentDiv.appendChild(btnDiv);
                        // Added SVG and Line to the HTML
                        showItems.appendChild(parentDiv);
                        // Added event listner to Remove SVG
                        svgDiv.addEventListener("click", (e) => {
                            if (e.target.localName == "svg"){
                                e.target.parentElement.parentElement.remove();
                            }else{
                                e.target.parentElement.parentElement.parentElement.remove();
                            }
                            let index_selected = selectedItemsList.indexOf(parseInt(e.target.classList[0]));
                            if (quantitySelected[index_selected] == 1){
                                selectedItemsList.splice(index_selected, 1);
                                quantitySelected.splice(index_selected, 1);
                                itemsList.value = selectedItemsList;
                                quantity.value = quantitySelected;
                            }else{
                                quantitySelected[index_selected] -= 1;
                                quantity.value = quantitySelected;
                            }
                            // Reduce Total
                            let reduced_index = itemData.item_id.indexOf(parseInt(e.target.classList[0]));
                            total -= itemData.price[reduced_index];
                            total_block.innerHTML = `Total : ${total}`;
                            totalInput.value = total;
                        });
                        //Add Total
                        total += itemData.price[index];
                        total_block.innerHTML = `Total : ${total}`;
                        totalInput.value = total;
                    }
                    element.checked = false;
                    quantityId.value = 1;
                }
            });
            let fiveColsCheckBoxes = document.querySelectorAll(".fiveCols > div > input[type=checkbox]");
            fiveColsCheckBoxes.forEach(element => {
                if (element.checked == true){
                    let quantityId;
                    if (window.innerWidth > 1000){
                        quantityId = document.getElementById(`${element.id}_quantity`);
                    }else{
                        quantityId = document.getElementById(`${element.id}_quantity_inline`);
                    }
                    let selectedItemInt = element.id;
                    if (selectedItemsList.includes(parseInt(element.id))){
                        let indexOfSelected = selectedItemsList.indexOf(parseInt(element.id));
                        quantitySelected[indexOfSelected] += parseInt(quantityId.value);
                        quantity.value = quantitySelected;
                    }else{
                        selectedItemsList.push(parseInt(element.id));
                        quantitySelected.push(parseInt(quantityId.value));
                        itemsList.value = selectedItemsList;
                        quantity.value = quantitySelected;
                    }
                    for (let i = 0; i < parseInt(quantityId.value); i++){
                        let index = itemData.item_id.indexOf(parseInt(selectedItemInt));
                        // Craeted Element SVG and Line
                        const parentDiv = document.createElement("div");
                        const nameDiv = document.createElement("div");
                        const addedItem = document.createTextNode(`${itemData.name[index]} [${itemData.item_size[index]}]`);
                        nameDiv.appendChild(addedItem);
                        const btnDiv = document.createElement("div");
                        const svgDiv = document.createElementNS("http://www.w3.org/2000/svg", "svg");
                        svgDiv.setAttribute("viewBox", "0 0 100 100");
                        svgDiv.setAttribute("width", "20px");
                        svgDiv.classList.add(parseInt(selectedItemInt));
                        const line1 = document.createElementNS("http://www.w3.org/2000/svg", "line");
                        line1.setAttribute("x1", "10");
                        line1.setAttribute("x2", "80");
                        line1.setAttribute("y1", "20");
                        line1.setAttribute("y2", "80");
                        line1.setAttribute("stroke-width", "10");
                        line1.setAttribute("stroke-linecap", "round");
                        line1.setAttribute("stroke", "red");
                        line1.classList.add(parseInt(selectedItemInt));
                        const line2 = document.createElementNS("http://www.w3.org/2000/svg", "line");
                        line2.setAttribute("x1", "10");
                        line2.setAttribute("x2", "80");
                        line2.setAttribute("y1", "80");
                        line2.setAttribute("y2", "20");
                        line2.setAttribute("stroke-width", "10");
                        line2.setAttribute("stroke-linecap", "round");
                        line2.setAttribute("stroke", "red");
                        line2.classList.add(parseInt(selectedItemInt));
                        svgDiv.appendChild(line1);
                        svgDiv.appendChild(line2);
                        btnDiv.appendChild(svgDiv);
                        parentDiv.appendChild(nameDiv);
                        parentDiv.appendChild(btnDiv);
                        // Added SVG and Line to the HTML
                        showItems.appendChild(parentDiv);
                        // Added event listner to Remove SVG
                        svgDiv.addEventListener("click", (e) => {
                            if (e.target.localName == "svg"){
                                e.target.parentElement.parentElement.remove();
                            }else{
                                e.target.parentElement.parentElement.parentElement.remove();
                            }
                            let index_selected = selectedItemsList.indexOf(parseInt(e.target.classList[0]));
                            if (quantitySelected[index_selected] == 1){
                                selectedItemsList.splice(index_selected, 1);
                                quantitySelected.splice(index_selected, 1);
                                itemsList.value = selectedItemsList;
                                quantity.value = quantitySelected;
                            }else{
                                quantitySelected[index_selected] -= 1;
                                quantity.value = quantitySelected;
                            }
                            // Reduce Total
                            let reduced_index = itemData.item_id.indexOf(parseInt(e.target.classList[0]));
                            total -= itemData.price[reduced_index];
                            total_block.innerHTML = `Total : ${total}`;
                            totalInput.value = total;
                        });
                        //Add Total
                        total += itemData.price[index];
                        total_block.innerHTML = `Total : ${total}`;
                        totalInput.value = total;
                    }
                    element.checked = false;
                    quantityId.value = 1;
                }
            });
        });
    }).catch(error => {
        console.log(error);
    });
}).catch(error => {
    console.log(error);
});
let paymentType = document.getElementById("PaymentType");
getPaymentModes().then(data => {
    let paymentData = JSON.parse(data);
    let html = "";
    paymentData.payment_mode.forEach((element, count) => {
        html += `<option value="${paymentData.payment_id[count]}">${element}</option>`;
    });
    paymentType.innerHTML += html;
}).catch(error => {
    console.log(error);
});
let additemBtn = document.getElementById("addItemsBtn");
additemBtn.addEventListener("click", () => {
    ItemsDiv.style.display='block';
    orderSection.style.display='none';
    let searchItem = document.getElementById('search-item');
    searchItem.addEventListener('input', ()=>{
        let mainCategory = document.querySelectorAll('.mainCategory');
        let fiveColName = document.querySelectorAll('.fiveColName');
        let threeColName = document.querySelectorAll('.threeColName');
        if(searchItem.value!=''){
            let mainCategoryDict = {};
            mainCategory.forEach(ele =>{
                ele.style.display='none';
                mainCategoryDict[ele.innerHTML] = false;
            });
            fiveColName.forEach(element => {
                let indexOfEle = itemData.name.indexOf(element.innerHTML);
                if (element.innerHTML.toLowerCase().includes(searchItem.value.toLowerCase())){
                    if (mainCategoryDict[itemData.maincategory[indexOfEle]] == false){
                        element.parentElement.style.display='grid';
                        mainCategoryDict[itemData.maincategory[indexOfEle]] = true;
                    }
                }else{
                    if (mainCategoryDict[itemData.maincategory[indexOfEle]] == false){
                        element.parentElement.style.display='none';
                    }
                }
            });
            threeColName.forEach(element => {
                let indexOfEle = itemData.name.indexOf(element.innerHTML);
                if (element.innerHTML.toLowerCase().includes(searchItem.value.toLowerCase())){
                    if (mainCategoryDict[itemData.maincategory[indexOfEle]] == false){
                        element.parentElement.style.display='grid';
                        mainCategoryDict[itemData.maincategory[indexOfEle]] = true;
                    }
                }else{
                    if (mainCategoryDict[itemData.maincategory[indexOfEle]] == false){
                        element.parentElement.style.display='none';
                    }
                }
            });
        }else{
            mainCategory.forEach(ele =>{
                ele.style.display='block';
            });
            fiveColName.forEach(element => {
                element.parentElement.style.display='grid';
            });
            threeColName.forEach(element => {
                element.parentElement.style.display='grid';
            });
        }
    });
});
paymentType.addEventListener("change", () => {
    let cols = document.getElementsByClassName("displayNone");
    if (paymentType.value == "3") {
        for (let i = 0; i < cols.length; i++) {
            cols[i].style.display = "block";
        }
    } else {
        for (let i = 0; i < cols.length; i++) {
            cols[i].style.display = "none";
        }
    }
});
let cashPaymentTotal = document.querySelector("#cashPaymentTotal > input");
let onlinePaymentTotal = document.querySelector("#onlinePaymentTotal > input");
let orderForm = document.getElementById("OrderForm");
orderForm.addEventListener("submit", (e) => {
    e.preventDefault();
    if (paymentType.value == 3) {
        if (cashPaymentTotal.value != "" || onlinePaymentTotal.value != "") {
            let cash = parseInt(cashPaymentTotal.value);
            let online = parseInt(onlinePaymentTotal.value);
            if (cash + online != total) {
                alert("Cash and Online should be equal to Total");
            }
            else {
                if (selectedItemsList.length != 0) {
                    alert("Order Received");
                    orderForm.submit();
                }
                else {
                    alert("Please Select at least one item")
                }
            }
        } else {
            alert("Please Enter value in Cash and Online Textbox")
        }
    }
    else {
        if (selectedItemsList.length != 0) {
            alert("Order Received");
            orderForm.submit();
        }
        else {
            alert("Please Select at least one item")
        }
    }
});