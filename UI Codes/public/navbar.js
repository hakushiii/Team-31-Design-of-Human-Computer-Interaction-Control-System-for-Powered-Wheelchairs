// JavaScript function to create a Bootstrap navbar
function createNavbar() {
  // Create navbar element
  const navbar = document.createElement('nav');
  navbar.classList.add('navbar', 'navbar-expand-sm', 'navbar-dark', 'bg-dark', 'shadow-sm', 'pt-1', 'pb-1', 'd-flex', 'justify-content-between', 'align-items-center');

  // Create a row for the grid system
  const row = document.createElement('div');
  row.classList.add('row', 'w-100', 'align-items-center'); // Updated to center items vertically

  // Create a column for the back button
  const backButtonColumn = document.createElement('div');
  backButtonColumn.classList.add('col-auto');

  // Create back button on the left (using navbar-toggler for toggle behavior)
  const backButton = document.createElement('button');
  backButton.classList.add('navbar-toggler', 'border-0'); // Add this line to remove the button border
  backButton.type = 'button';

  // Style the button to make it smaller
  backButton.style.padding = '0.2rem 0.5rem'; // Adjust padding to make it smaller
  backButton.style.display = 'flex';
  backButton.style.alignItems = 'center';

  // Create an image element for the back button
  const backImage = document.createElement('img');
  backImage.src = 'icons/back.png';
  backImage.alt = 'back'; // Add alternative text for accessibility

  // Set the width and height attributes for the image
  backImage.width = 18;
  backImage.height = 18;

  // Make the image non-draggable
  backImage.draggable = false;

  // Center the image within the button
  backImage.style.display = 'block';
  backImage.style.margin = 'auto';

  backButton.appendChild(backImage);
  backButton.addEventListener('click', goBack); // Add click event to call goBack() function

  // Add back button to the column
  backButtonColumn.appendChild(backButton);

  // Create a column for the logo and center it with less padding
  const logoColumn = document.createElement('div');
  logoColumn.classList.add('col', 'text-center');
  logoColumn.style.paddingLeft = '0px'; // Adjust the value as needed for less padding

  // Create logo in the center
  const logo = document.createElement('a');
  logo.classList.add('navbar-brand');

  // Create an image element for the logo
  const logoImage = document.createElement('img');
  logoImage.src = 'icons/biopin_logo2.png';
  logoImage.alt = 'Logo'; // Add alternative text for accessibility

  // Set the width and height attributes for resizing
  logoImage.width = 40;
  logoImage.height = 40;

  // Make the image non-draggable
  logoImage.draggable = false;

  // Add the image to the logo
  logo.appendChild(logoImage);

  // Append logo to the column
  logoColumn.appendChild(logo);

  // Append columns to the row
  row.appendChild(backButtonColumn);
  row.appendChild(logoColumn);

  // Append row to the navbar directly
  navbar.appendChild(row);

  // Append navbar to the body
  document.body.appendChild(navbar);
}

// Example goBack() function
function goBack() {
  window.history.back();
}

// Call the function to create the navbar
createNavbar();
