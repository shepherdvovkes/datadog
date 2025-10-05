// Initialize Lucide icons
document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        lastScroll = currentScroll;
    });
    
    // Smooth scroll for navigation links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 70;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Smooth scroll for wiki navigation links
    const wikiNavLinks = document.querySelectorAll('.wiki-nav-link');
    wikiNavLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 100;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
                
                // Update active state
                wikiNavLinks.forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            }
        });
    });
    
    // Mobile menu toggle
    const menuToggle = document.getElementById('menuToggle');
    const navLinksContainer = document.querySelector('.nav-links');
    
    menuToggle.addEventListener('click', () => {
        navLinksContainer.classList.toggle('active');
    });
    
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe all cards including new wiki elements and ML pipeline elements
    const cards = document.querySelectorAll('.mission-card, .value-card, .uav-card, .nato-card, .capability-card, .stat-item, .standard-card, .wiki-section, .resource-card, .timeline-item, .ml-module-card, .flow-stage, .infra-card, .tech-category, .compliance-card');
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
    
    // Counter animation for hero stats
    const animateValue = (element, start, end, duration) => {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const value = Math.floor(progress * (end - start) + start);
            element.textContent = value;
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    };
    
    // Parallax effect for hero section
    const hero = document.querySelector('.hero');
    if (hero) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const parallax = scrolled * 0.5;
            hero.style.transform = `translateY(${parallax}px)`;
        });
    }
    
    // Active nav link on scroll
    const sections = document.querySelectorAll('.section');
    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (window.pageYOffset >= (sectionTop - 200)) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
        
        // Update wiki nav links on scroll
        const wikiSections = document.querySelectorAll('.wiki-section');
        let currentWiki = '';
        wikiSections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (window.pageYOffset >= (sectionTop - 150)) {
                currentWiki = section.getAttribute('id');
            }
        });
        
        wikiNavLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentWiki}`) {
                link.classList.add('active');
            }
        });
    });
    
    // Tech stack badges hover effect
    const techBadges = document.querySelectorAll('.tech-badge');
    techBadges.forEach(badge => {
        badge.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
            this.style.transition = 'transform 0.2s ease';
        });
        badge.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    // Add ripple effect to cards
    const createRipple = (event) => {
        const card = event.currentTarget;
        const ripple = document.createElement('span');
        const rect = card.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        card.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    };
    
    const allCards = document.querySelectorAll('.mission-card, .value-card, .uav-card, .nato-card, .capability-card, .standard-card, .resource-card, .ml-module-card, .infra-card, .tech-category, .compliance-card');
    allCards.forEach(card => {
        card.style.position = 'relative';
        card.style.overflow = 'hidden';
        card.addEventListener('click', createRipple);
    });
    
    // Add ripple CSS
    const style = document.createElement('style');
    style.textContent = `
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(59, 130, 246, 0.3);
            transform: scale(0);
            animation: ripple-animation 0.6s ease-out;
            pointer-events: none;
        }
        
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        .nav-link.active {
            color: var(--text-primary);
        }
        
        .nav-link.active::after {
            width: 100%;
        }
        
        .wiki-nav-link.active {
            background-color: rgba(59, 130, 246, 0.15);
            border-color: var(--accent);
            color: var(--text-primary);
        }
        
        @media (max-width: 968px) {
            .nav-links.active {
                display: flex;
                flex-direction: column;
                position: absolute;
                top: 70px;
                left: 0;
                right: 0;
                background-color: rgba(10, 14, 26, 0.98);
                padding: 2rem;
                border-bottom: 1px solid var(--border-color);
                gap: 1rem;
            }
            
            .lang-switcher {
                justify-content: center;
                width: 100%;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Cursor trail effect (subtle)
    let lastX = 0;
    let lastY = 0;
    let trails = [];
    
    document.addEventListener('mousemove', (e) => {
        const dx = e.clientX - lastX;
        const dy = e.clientY - lastY;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance > 10 && trails.length < 5) {
            const trail = document.createElement('div');
            trail.className = 'cursor-trail';
            trail.style.left = e.clientX + 'px';
            trail.style.top = e.clientY + 'px';
            document.body.appendChild(trail);
            trails.push(trail);
            
            setTimeout(() => {
                trail.remove();
                trails = trails.filter(t => t !== trail);
            }, 500);
        }
        
        lastX = e.clientX;
        lastY = e.clientY;
    });
    
    // Add cursor trail CSS
    const cursorStyle = document.createElement('style');
    cursorStyle.textContent = `
        .cursor-trail {
            position: fixed;
            width: 4px;
            height: 4px;
            background: var(--accent);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            opacity: 0.5;
            animation: trail-fade 0.5s ease-out forwards;
        }
        
        @keyframes trail-fade {
            to {
                opacity: 0;
                transform: scale(0);
            }
        }
    `;
    document.head.appendChild(cursorStyle);
    
    // Re-initialize Lucide icons for dynamically loaded content
    const reinitializeIcons = () => {
        lucide.createIcons();
    };
    
    // Call reinitialize after a short delay to ensure all content is loaded
    setTimeout(reinitializeIcons, 100);
    
    // Hover effect for resource cards
    const resourceCards = document.querySelectorAll('.resource-card');
    resourceCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const icon = this.querySelector('svg');
            if (icon) {
                icon.style.transform = 'scale(1.2) rotate(5deg)';
                icon.style.transition = 'transform 0.3s ease';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            const icon = this.querySelector('svg');
            if (icon) {
                icon.style.transform = 'scale(1) rotate(0deg)';
            }
        });
    });
    
    // Add expand/collapse functionality for standard cards
    const standardCards = document.querySelectorAll('.standard-card');
    standardCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Don't toggle if clicking on a link
            if (e.target.tagName === 'A') return;
            
            const details = this.querySelector('.standard-details');
            if (details) {
                const isExpanded = details.style.maxHeight && details.style.maxHeight !== '0px';
                
                if (isExpanded) {
                    details.style.maxHeight = '0px';
                    details.style.opacity = '0';
                    details.style.marginTop = '0';
                    details.style.paddingTop = '0';
                } else {
                    details.style.maxHeight = details.scrollHeight + 'px';
                    details.style.opacity = '1';
                    details.style.marginTop = '1.5rem';
                    details.style.paddingTop = '1.5rem';
                }
            }
        });
    });
    
    // Animate metric bars on scroll
    const metricBars = document.querySelectorAll('.metric-bar');
    const metricObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, { threshold: 0.5 });
    
    metricBars.forEach(bar => {
        metricObserver.observe(bar);
    });
    
    // Hover effects for flow stages
    const flowStages = document.querySelectorAll('.flow-stage');
    flowStages.forEach((stage, index) => {
        stage.style.animationDelay = `${index * 0.1}s`;
    });
    
    console.log('DATADOG Intelligence Platform initialized');
    console.log('NATO Standards Wiki Module loaded');
    console.log('ML Pipeline Module loaded');
    console.log('Slava Ukraini!');
});

// Language switching function
function switchLanguage(lang) {
    const languageMap = {
        'uk': 'index.html',
        'en': 'index-en.html',
        'ja': 'index-ja.html'
    };
    
    if (languageMap[lang]) {
        window.location.href = languageMap[lang];
    }
}

