'use strict';

/**
 * security-question service
 */

const { createCoreService } = require('@strapi/strapi').factories;

module.exports = createCoreService('api::security-question.security-question');
