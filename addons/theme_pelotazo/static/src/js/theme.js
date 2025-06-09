/** @odoo-module **/

import publicWidget from '@web/legacy/js/public/public_widget';
import { _t } from '@web/core/l10n/translation';
    
// Safe selector function
const safeSelector = function(selector, context) {
    try {
        return $(selector, context || document);
    } catch (e) {
        console.warn('Error in selector:', selector, e);
        return $([]);
    }
};

// Safe replace function
const safeReplace = function(str, pattern, replacement) {
    return (str || '').toString().replace(pattern, replacement);
};
    
    // Define our frontend features
    publicWidget.registry.PelotazoAnimation = publicWidget.Widget.extend({
        selector: '.s_banner',
        events: {
            'click a[href*="#"]:not([href="#"])': '_onAnchorClick'
        },
        
        start: function () {
            try {
                // Safely add animation class
                if (this.$el.length) {
                    this.$el.addClass('animated fadeIn');
                }
                
                // Initialize other features
                this._initScrollReveal();
                this._initSmoothScroll();
                
                return this._super.apply(this, arguments);
            } catch (e) {
                console.error('Error in PelotazoAnimation:', e);
                return this._super.apply(this, arguments);
            }
        },
        
        _initScrollReveal: function () {
            try {
                if (typeof ScrollReveal !== 'undefined') {
                    var sr = ScrollReveal();
                    if (sr.reveal) {
                        sr.reveal('.s_banner h1', { 
                            delay: 200,
                            distance: '50px',
                            origin: 'bottom',
                            duration: 1000,
                            easing: 'cubic-bezier(0.5, 0, 0, 1)',
                            reset: false
                        });
                        
                        sr.reveal('.s_banner .lead', { 
                            delay: 400,
                            distance: '50px',
                            origin: 'bottom',
                            duration: 1000,
                            easing: 'cubic-bezier(0.5, 0, 0, 1)',
                            reset: false
                        });
                    }
                }
            } catch (e) {
                console.warn('ScrollReveal initialization failed:', e);
            }
        },
        
        _onAnchorClick: function(ev) {
            try {
                var $target = $(ev.currentTarget);
                var hash = $target.attr('href');
                
                if (!hash || hash === '#') {
                    return true;
                }
                
                var targetEl = $(hash);
                if (targetEl.length) {
                    ev.preventDefault();
                    $('html, body').animate({
                        scrollTop: targetEl.offset().top
                    }, 800);
                }
            } catch (e) {
                console.warn('Error in smooth scroll:', e);
            }
        },
        
        _initSmoothScroll: function () {
            // Manejado por el event handler _onAnchorClick
        }
    });
    
    return {
        PelotazoAnimation: publicWidget.registry.PelotazoAnimation
    };

// Initialize when DOM is ready
$(document).ready(function() {
    try {
        // Any additional initialization can go here
        console.log('Theme Pelotazo initialized successfully');
    } catch (e) {
        console.error('Error initializing Theme Pelotazo:', e);
    }
});
