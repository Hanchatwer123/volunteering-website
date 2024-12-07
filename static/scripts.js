document.addEventListener("DOMContentLoaded", function () {
    // Select all elements that should fade in
    const fadeElements = document.querySelectorAll('.fade-in');

    // If no fade-in elements exist, exit early
    if (fadeElements.length === 0) return;

    // IntersectionObserver options
    const options = {
        root: null,  // Use the viewport as the root
        threshold: 0.1 // Trigger when at least 10% of the element is visible
    };

    // IntersectionObserver callback function
    const fadeInObserver = new IntersectionObserver(function (entries, observer) {
        entries.forEach(entry => {
            // Check if the entry is in view
            if (entry.isIntersecting) {
                // Add the 'fade-in-visible' class to trigger the fade-in animation
                entry.target.classList.add('fade-in-visible');
                // Stop observing the current element to improve performance
                observer.unobserve(entry.target);
            }
        });
    }, options);

    // Observe each fade-in element
    fadeElements.forEach(element => {
        fadeInObserver.observe(element);
    });
});
