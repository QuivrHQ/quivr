'use strict';

/**
 * demo-video service
 */

const { createCoreService } = require('@strapi/strapi').factories;

module.exports = createCoreService('api::demo-video.demo-video');
