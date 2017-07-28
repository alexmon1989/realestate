# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-23 13:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_vhousesfortables'),
    ]

    operations = [
        migrations.RunSQL(
            '''
            DROP VIEW IF EXISTS `v_houses_for_tables`;
            CREATE VIEW `v_houses_for_tables` AS SELECT
               	`house`.`house_id` AS `house_id`,
                `suburb`.`name` AS `suburb_name`,
                `house`.`suburb_id` AS `suburb_id`,
                `city`.`city_name` AS `city_name`,
                `region`.`name` AS `region_name`,
                `house`.`street_number` AS `street_number`,
                `house`.`street_name` AS `street_name`,
                (
                    CASE
                    WHEN (
                        (
                            `house`.`street_number` <> ''
                        )
                        AND (`house`.`street_name` <> '')
                    ) THEN
                        concat_ws(
                            ' ',
                            `house`.`street_number`,
                            `house`.`street_name`
                        )
                    ELSE
                        'Address not specified'
                    END
                ) AS `address`,
                `house`.`price` AS `price`,
                `house`.`price_type_id` AS `price_type_id`,
                CASE
            WHEN (`house`.`price` <> 0) THEN
                CONCAT(
                    '$',
                    FORMAT(`house`.`price`, 0)
                )
            ELSE
                `pricing_method`.`name`
            END AS `price_with_price_type`,
             `house`.`government_value` AS `government_value`,
             `house`.`government_to_price` AS `government_to_price`,
             `house`.`bedrooms` AS `bedrooms`,
             `house`.`bathrooms` AS `bathrooms`,
             `house`.`land` AS `land`,
             `house`.`floor` AS `floor`,
             `house`.`property_type_id` AS `property_type_id`,
             CASE
            WHEN (`house`.`bedrooms` > 0) THEN
                concat_ws(
                    ' bedroom ',
                    `house`.`bedrooms`,
                    `property_type`.`name`
                )
            ELSE
                `property_type`.`name`
            END AS `property_type_full`,
             `house`.`description` AS `description`,
             `house`.`car_spaces` AS `car_spaces`,
             `house`.`ensuite` AS `ensuite`,
             `house`.`photos` AS `photos`,
             `house`.`listing_create_date` AS `listing_create_date`,
             `house`.`create_time` AS `create_time`,
             `open_homes`.`date_from` AS `open_homes_from`,
             `open_homes`.`date_to` AS `open_homes_to`,
             `agent`.`name` AS `agent_name`,
             `agent`.`ddi_phone` AS `agent_ddi_phone`,
             `agent`.`email` AS `agent_email`,
             `agent`.`mobile_phone` AS `agent_mobile_phone`,
             `agent`.`work_phone` AS `agent_work_phone`,
             `agency`.`agency_name` AS `agency_name`,
             `agency`.`email` AS `agency_email`,
             `agency`.`work_phone` AS `agency_work_phone`
            FROM
                `house`
            JOIN `suburb` ON `house`.`suburb_id` = `suburb`.`id`
            JOIN `city` ON `suburb`.`city_id` = `city`.`city_id`
            JOIN `region` ON `city`.`region_id` = `region`.`id`
            JOIN `property_type` ON `house`.`property_type_id` = `property_type`.`id`
            JOIN `pricing_method` ON `house`.`price_type_id` = `pricing_method`.`id`
            LEFT JOIN `open_homes` ON `house`.`house_id` = `open_homes`.`house_id`
            LEFT JOIN `agenthouse` ON (
                `house`.`house_id` = `agenthouse`.`house_id`
            )
            LEFT JOIN `agent` ON (
                `agenthouse`.`agent_id` = `agent`.`agent_id`
            )
            LEFT JOIN `agencyhouse` ON (
                `house`.`house_id` = `agencyhouse`.`house_id`
            )
            LEFT JOIN `agency` ON (
                `agencyhouse`.`agency_id` = `agencyhouse`.`agency_id`
            );
            '''
        ),
    ]
