async function getCategory(){
    const response = await fetch("/getCategory/");
    let data = await response.json();
    return data;
};
async function getSize(){
    const response = await fetch("/getSize/");
    let data = await response.json();
    return data;
};
async function getMainCategory(){
    const response = await fetch("/getMainCategory/");
    let data = await response.json();
    return data;
};
getCategory().then(data => {
    let category_data = JSON.parse(data);
    let html = "";
    category_data.category.forEach((element, count) => {
        html += `<option value="${category_data.category_id[count]}">${element}</option>`;
    });
    document.getElementById("Category").innerHTML += html;
}).catch(error => {
    console.log(error);
});
getSize().then(data => {
    let size_data = JSON.parse(data);
    let html = "";
    size_data.item_size.forEach((element, count) => {
        html += `<option value="${size_data.size_id[count]}">${element}</option>`;
    });
    document.getElementById("Size").innerHTML += html;
}).catch(error => {
    console.log(error);
});
getMainCategory().then(data => {
    let mainCategory_data = JSON.parse(data);
    let html = "";
    mainCategory_data.forEach(element => {
        html += `<option value="${element}">${element}</option>`;
    });
    document.getElementById("mainCategoryId").innerHTML += html;
}).catch(error => {
    console.log(error);
});