const vehicleTypeSelect = document.getElementById("vehicle-type");
const customFieldsContainer = document.getElementById(
  "custom-fields-container"
);

// Hide the custom fields container initially
customFieldsContainer.style.display = "none";

vehicleTypeSelect.addEventListener("change", () => {
  if (vehicleTypeSelect.value === "custom") {
    // Show the custom fields container if the custom option is selected
    customFieldsContainer.style.display = "block";
  } else {
    // Hide the custom fields container if the regular option is selected
    customFieldsContainer.style.display = "none";
  }
});
