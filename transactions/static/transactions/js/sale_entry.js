// Sale Entry JavaScript Logic

document.addEventListener("DOMContentLoaded", function() {
    // Set default date and time if not present
    if (!document.getElementById('invDate').value) {
        document.getElementById('invDate').valueAsDate = new Date();
    }
    const now = new Date();
    document.getElementById('invTime').value = now.toTimeString().slice(0, 5);

    // Initialize form with data from Django (passed via JSON script tag)
    const dataScript = document.getElementById('sale-data');
    const initialSaleData = dataScript ? JSON.parse(dataScript.textContent) : null;

    if (initialSaleData && initialSaleData.isEditing) {
        initializeEditMode(initialSaleData);
    }
});

function initializeEditMode(data) {
    // Populate Party
    const partySelect = document.getElementById('partySelect');
    if (partySelect) {
        partySelect.value = data.partyName;
        document.getElementById('partyAdd1').value = data.partyDetails.add1;
        document.getElementById('partyAdd2').value = data.partyDetails.add2;
        document.getElementById('partyCity').value = data.partyDetails.city;
        document.getElementById('partyMobile').value = data.partyDetails.mobile;
        document.getElementById('partyEmail').value = data.partyDetails.email;
    }

    // Populate Items
    const tbody = document.getElementById('itemsTable').querySelector('tbody');
    data.items.forEach(detail => {
        addItemRow(tbody, detail);
    });
    
    // Calculate totals after populating
    calculateFooterTotals();
}

function addItemRow(tbody, detail) {
    const rowCount = tbody.rows.length + 1;
    const newRow = tbody.insertRow();
    newRow.setAttribute('onclick', 'editRow(this)');
    newRow.style.cursor = 'pointer';
    newRow.innerHTML = `
        <td class="text-center">${rowCount}</td>
        <td>${detail.item}</td>
        <td class="text-end">${detail.qty}</td>
        <td class="text-end">${parseFloat(detail.rate).toFixed(2)}</td>
        <td class="text-end">${parseFloat(detail.amount).toFixed(2)}</td>
        <td class="text-center">
            <button class="btn btn-sm btn-outline-danger py-0 border-0" onclick="deleteRow(event, this)">X</button>
        </td>
    `;
}

// --- State Management ---
let currentRowIndex = -1; // -1 means new item, otherwise index of row being edited

// --- API Calls ---
function fetchPartyDetails() {
    const partyName = document.getElementById('partySelect').value;
    if (!partyName) {
        clearPartyDetails();
        return;
    }
    fetch(`/api/party-details/?party_name=${encodeURIComponent(partyName)}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('partyAdd1').value = data.add1 || '';
            document.getElementById('partyAdd2').value = data.add2 || '';
            document.getElementById('partyCity').value = data.city || '';
            document.getElementById('partyMobile').value = data.mobile || '';
            document.getElementById('partyEmail').value = data.email || '';
        });
}

function clearPartyDetails() {
    document.getElementById('partyAdd1').value = '';
    document.getElementById('partyAdd2').value = '';
    document.getElementById('partyCity').value = '';
    document.getElementById('partyMobile').value = '';
    document.getElementById('partyEmail').value = '';
}

function fetchItemDetails() {
    const itemName = document.getElementById('itemSelect').value;
    if (!itemName) return;
    
    fetch(`/api/item-details/?item_name=${encodeURIComponent(itemName)}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('itemRate').value = data.rate || 0;
            calculateItemAmount();
            document.getElementById('itemQty').focus();
        });
}

// --- Calculations ---
function calculateItemAmount() {
    const qty = parseFloat(document.getElementById('itemQty').value) || 0;
    const rate = parseFloat(document.getElementById('itemRate').value) || 0;
    document.getElementById('itemAmount').value = (qty * rate).toFixed(2);
}

// --- Grid Operations ---
function addOrUpdateItem() {
    const item = document.getElementById('itemSelect').value;
    const qty = parseFloat(document.getElementById('itemQty').value);
    const rate = parseFloat(document.getElementById('itemRate').value);
    const amount = parseFloat(document.getElementById('itemAmount').value);

    if (!item || !qty || !rate) {
        alert("Please fill all item details.");
        return;
    }

    const tbody = document.getElementById('itemsTable').querySelector('tbody');

    if (currentRowIndex >= 0) {
        // Update existing row
        const row = tbody.rows[currentRowIndex];
        row.cells[1].innerText = item;
        row.cells[2].innerText = qty;
        row.cells[3].innerText = rate.toFixed(2);
        row.cells[4].innerText = amount.toFixed(2);
        
        // Reset state
        currentRowIndex = -1;
        document.getElementById('btnAddItem').innerText = "Add";
        document.getElementById('btnAddItem').classList.remove('btn-warning');
        document.getElementById('btnAddItem').classList.add('btn-primary');
    } else {
        // Add new row using helper
        addItemRow(tbody, { item, qty, rate, amount });
    }

    clearItemInput();
    calculateFooterTotals();
}

function editRow(row) {
    currentRowIndex = row.rowIndex - 1; // Adjust for header
    const cells = row.cells;
    
    document.getElementById('itemSelect').value = cells[1].innerText;
    document.getElementById('itemQty').value = cells[2].innerText;
    document.getElementById('itemRate').value = cells[3].innerText;
    document.getElementById('itemAmount').value = cells[4].innerText;
    
    // Change button to Update
    const btn = document.getElementById('btnAddItem');
    btn.innerText = "Update";
    btn.classList.remove('btn-primary');
    btn.classList.add('btn-warning');
}

function deleteRow(event, btn) {
    event.stopPropagation(); // Prevent row click (edit)
    const row = btn.parentNode.parentNode;
    row.parentNode.removeChild(row);
    
    // Re-number rows
    const tbody = document.getElementById('itemsTable').querySelector('tbody');
    for (let i = 0; i < tbody.rows.length; i++) {
        tbody.rows[i].cells[0].innerText = i + 1;
    }
    
    calculateFooterTotals();
}

function clearItemInput() {
    document.getElementById('itemSelect').value = "";
    document.getElementById('itemQty').value = "";
    document.getElementById('itemRate').value = "";
    document.getElementById('itemAmount').value = "";
    currentRowIndex = -1;
    const btn = document.getElementById('btnAddItem');
    btn.innerText = "Add";
    btn.classList.remove('btn-warning');
    btn.classList.add('btn-primary');
    document.getElementById('itemSelect').focus();
}

function calculateFooterTotals() {
    const tbody = document.getElementById('itemsTable').querySelector('tbody');
    let subTotal = 0;
    for (let i = 0; i < tbody.rows.length; i++) {
        subTotal += parseFloat(tbody.rows[i].cells[4].innerText);
    }
    document.getElementById('subTotal').value = subTotal.toFixed(2);
    calculateFinalTotal();
}

function calculateFinalTotal(source) {
    const subTotal = parseFloat(document.getElementById('subTotal').value) || 0;
    let discountPer = parseFloat(document.getElementById('discountPer').value) || 0;
    let discountAmt = parseFloat(document.getElementById('discountAmt').value) || 0;
    const adjustment = parseFloat(document.getElementById('adjustment').value) || 0;

    if (source === 'amt') {
        // Calculate % from Amt
        discountPer = (discountAmt / subTotal) * 100;
        document.getElementById('discountPer').value = subTotal > 0 ? discountPer.toFixed(2) : 0;
    } else {
        // Calculate Amt from %
        discountAmt = (subTotal * discountPer) / 100;
        document.getElementById('discountAmt').value = discountAmt.toFixed(2);
    }

    const netAmount = subTotal - discountAmt + adjustment;
    document.getElementById('netAmount').value = netAmount.toFixed(2);
    convertNumberToWords(netAmount);
}

function convertNumberToWords(amount) {
    if (!amount || isNaN(amount)) {
        document.getElementById('amountInWords').value = "";
        return;
    }

    const words = new Array();
    words[0] = '';
    words[1] = 'One';
    words[2] = 'Two';
    words[3] = 'Three';
    words[4] = 'Four';
    words[5] = 'Five';
    words[6] = 'Six';
    words[7] = 'Seven';
    words[8] = 'Eight';
    words[9] = 'Nine';
    words[10] = 'Ten';
    words[11] = 'Eleven';
    words[12] = 'Twelve';
    words[13] = 'Thirteen';
    words[14] = 'Fourteen';
    words[15] = 'Fifteen';
    words[16] = 'Sixteen';
    words[17] = 'Seventeen';
    words[18] = 'Eighteen';
    words[19] = 'Nineteen';
    words[20] = 'Twenty';
    words[30] = 'Thirty';
    words[40] = 'Forty';
    words[50] = 'Fifty';
    words[60] = 'Sixty';
    words[70] = 'Seventy';
    words[80] = 'Eighty';
    words[90] = 'Ninety';

    amount = amount.toString();
    var atemp = amount.split(".");
    var number = atemp[0].split(",").join("");
    var n_length = number.length;
    var words_string = "";
    
    if (n_length <= 9) {
        var n_array = new Array(0, 0, 0, 0, 0, 0, 0, 0, 0);
        var received_n_array = new Array();
        for (var i = 0; i < n_length; i++) {
            received_n_array[i] = number.substr(i, 1);
        }
        for (var i = 9 - n_length, j = 0; i < 9; i++, j++) {
            n_array[i] = received_n_array[j];
        }
        for (var i = 0, j = 1; i < 9; i++, j++) {
            if (i == 0 || i == 2 || i == 4 || i == 7) {
                if (n_array[i] == 1) {
                    n_array[j] = 10 + parseInt(n_array[j]);
                    n_array[i] = 0;
                }
            }
        }
        
        value = "";
        for (var i = 0; i < 9; i++) {
            if (i == 0 || i == 2 || i == 4 || i == 7) {
                value = n_array[i] * 10;
            } else {
                value = n_array[i];
            }
            if (value != 0) {
                words_string += words[value] + " ";
            }
            if ((i == 1 && value != 0) || (i == 0 && value != 0 && n_array[i + 1] == 0)) {
                words_string += "Crores ";
            }
            if ((i == 3 && value != 0) || (i == 2 && value != 0 && n_array[i + 1] == 0)) {
                words_string += "Lakhs ";
            }
            if ((i == 5 && value != 0) || (i == 4 && value != 0 && n_array[i + 1] == 0)) {
                words_string += "Thousand ";
            }
            if (i == 6 && value != 0 && (n_array[i + 1] != 0 && n_array[i + 2] != 0)) {
                words_string += "Hundred and ";
            } else if (i == 6 && value != 0) {
                words_string += "Hundred ";
            }
        }
        words_string = words_string.split("  ").join(" ");
    }
    
    document.getElementById('amountInWords').value = words_string + "Only"; 
}

function saveSale() {
    const invNo = document.getElementById('invNo').value;
    const invDate = document.getElementById('invDate').value;
    const partyName = document.getElementById('partySelect').value;
    const subTotal = parseFloat(document.getElementById('subTotal').value) || 0;
    const discountPer = parseFloat(document.getElementById('discountPer').value) || 0;
    const discountAmt = parseFloat(document.getElementById('discountAmt').value) || 0;
    const adjustment = parseFloat(document.getElementById('adjustment').value) || 0;
    const netAmount = parseFloat(document.getElementById('netAmount').value) || 0;
    const remark = document.getElementById('remarks').value;
    const amountInWords = document.getElementById('amountInWords').value;

    // Validations
    if (!partyName) { alert("Please select a Party."); return; }
    
    const items = [];
    const tbody = document.getElementById('itemsTable').querySelector('tbody');
    if (tbody.rows.length === 0) { alert("Please add at least one item."); return; }

    for (let i = 0; i < tbody.rows.length; i++) {
        const row = tbody.rows[i];
        items.push({
            item_name: row.cells[1].innerText,
            qty: parseFloat(row.cells[2].innerText),
            rate: parseFloat(row.cells[3].innerText),
            amount: parseFloat(row.cells[4].innerText)
        });
    }

    const payload = {
        inv_no: invNo,
        inv_date: invDate,
        party_name: partyName,
        sub_total: subTotal,
        discount_per: discountPer,
        discount_amt: discountAmt,
        adjustment: adjustment,
        net_amount: netAmount,
        remark: remark,
        amount_in_words: amountInWords,
        
        // Party Snapshot
        add1: document.getElementById('partyAdd1').value,
        add2: document.getElementById('partyAdd2').value,
        city: document.getElementById('partyCity').value,
        mobile: document.getElementById('partyMobile').value,
         
        items: items
    };

    fetch('/sale/save/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(data.message);
            window.location.href = '/sale/list/'; 
        } else {
            alert("Error: " + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}
