package com.stockTracker.congressWatch.importer.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;

public class ImporterController {

    @Autowired
    MongoTemplate mongoTemplate;

    public int updateDomain(String domain, boolean displayAds) {

//        Query query = new Query(Criteria.where("domain").is(domain));
        Update update = new Update();
        update.set("displayAds", displayAds);

        WriteResult result = mongoTemplate.updateFirst(query, update, Domain.class);

        if(result!=null)
            return result.getN();
        else
            return 0;

    }
}