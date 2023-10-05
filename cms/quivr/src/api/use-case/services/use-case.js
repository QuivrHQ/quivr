'use strict';

/**
 * use-case service
 */

const { createCoreService } = require('@strapi/strapi').factories;

module.exports = createCoreService('api::use-case.use-case');
