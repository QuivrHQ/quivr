'use strict';

/**
 * blog service
 */

const { createCoreService } = require('@strapi/strapi').factories;

module.exports = createCoreService('api::blog.blog');
