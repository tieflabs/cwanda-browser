	    let button = document.getElementById('button');
		button.addEventListener('click', function() {
			for(let i = 0; i < 50; i++){
			let spark = document.createElement('i');
			spark.classList.add('spark');


			// difference possition for each spark element
			const randomX = (Math.random() - 0.5) * window.innerWidth;
			const randomY = (Math.random() - 0.5) * window.innerHeight;
			spark.style.setProperty('--x', randomX + 'px');
			spark.style.setProperty('--y', randomY + 'px');

			// difference size for each spark element
			const randomSize = Math.random() * 12 + 6;
			spark.style.height = randomSize + 'px';
			spark.style.width = randomSize + 'px';

			// Add animation difference duration
			const duration = Math.random() * 1.5 + 0.5;
			spark.style.animation = `alt ${duration}s ease-out forwards`;

			document.body.appendChild(spark);

			// remove spark elements aftter 1.5s
			setTimeout(function(){
				spark.remove();
			},1500);

			}
		})
