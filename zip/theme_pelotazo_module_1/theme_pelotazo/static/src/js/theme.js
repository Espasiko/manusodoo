/* Theme Pelotazo JS */
odoo.define('theme_pelotazo.frontend', function (require) {
    'use strict';
    
    // Import required modules
    var publicWidget = require('web.public.widget');
    
    // Define our frontend features
    publicWidget.registry.PelotazoAnimation = publicWidget.Widget.extend({
        selector: '.s_banner',
        events: {
            'click': '_onClick',
        },
        
        _onClick: function (ev) {
            console.log('Banner clicked!');
        },
    });
    
    // Register the widget
    publicWidget.registry.PelotazoAnimation.prototype.start = function () {
        console.log('Pelotazo theme initialized');
        return this._super.apply(this, arguments);
    };
});
