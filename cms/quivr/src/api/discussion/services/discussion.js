'use strict';

/**
 * discussion service
 */

const { createCoreService } = require('@strapi/strapi').factories;

module.exports = createCoreService('api::discussion.discussion');
