function updateClock() {
  // Get the current time
  let currentTime = new Date();

  // Extract hours, minutes, and seconds
  let hours = currentTime.getHours();
  let minutes = currentTime.getMinutes();
  let seconds = currentTime.getSeconds();

  // Pad single digit minutes and seconds with a leading zero
  minutes = (minutes < 10 ? "0" : "") + minutes;
  seconds = (seconds < 10 ? "0" : "") + seconds;

  // Determine whether it's AM or PM
  let period = (hours < 12) ? "AM" : "PM";

  // Convert the hours to 12-hour format
  hours = (hours > 12) ? hours - 12 : hours;
  hours = (hours === 0) ? 12 : hours;

  // Create the format: HH:MM:SS AM/PM
  let timeString = hours + ":" + minutes + ":" + seconds + " " + period;

  // Display the time
  document.getElementById("clock").textContent = timeString;
}

// Update the clock every second
setInterval(updateClock, 1000);

// Initial call to display the clock immediately
updateClock();
