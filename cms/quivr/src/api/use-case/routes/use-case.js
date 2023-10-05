'use strict';

/**
 * use-case router
 */

const { createCoreRouter } = require('@strapi/strapi').factories;

module.exports = createCoreRouter('api::use-case.use-case');
