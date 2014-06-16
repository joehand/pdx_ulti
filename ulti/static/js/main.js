/*! =======================================================================
 * Main JS
 * Author: JoeHand
 * ======================================================================== */

define([
    'backbone',
    'jquery',
    'underscore',
    'views/AppView',
    'models/AppModel',
], function (Backbone, $, _, AppView, AppModel) {

    var appView, appModel, NAMESPACE;

    NAMESPACE = ulti

    appModel = new AppModel(NAMESPACE);

    appView = new AppView({
        model      : appModel,
        el         : $('.document').get(0),
    });

});
