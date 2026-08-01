function editFurniture(id, name, price, unit, defaultQty, minQty, maxQty, required) {
  // 1. Modal dikhayein
  document.getElementById('editFurnitureModal').style.display = 'flex';

  // 2. Form fields me purana data bharein
  document.getElementById('edit_id').value = id;
  document.getElementById('edit_name').value = name;
  document.getElementById('edit_price').value = price;
  document.getElementById('edit_unit').value = unit;
  document.getElementById('edit_default').value = defaultQty;
  document.getElementById('edit_min').value = minQty || '';
  document.getElementById('edit_max').value = maxQty || '';
  document.getElementById('edit_required').checked = required;

  // 3. Action URL set karein (urls.py ke pattern 'furniture/edit/<id>/' se exact match)
  document.getElementById('editFurnitureForm').action = '/cms/furniture/edit/' + id + '/';
}

function closeFurnitureModal() {
  document.getElementById('editFurnitureModal').style.display = 'none';
}

// Modal ke bahar click karne par modal close karne ke liye
window.onclick = function (e) {
  let modal = document.getElementById('editFurnitureModal');
  if (e.target === modal) {
    modal.style.display = 'none';
  }
};