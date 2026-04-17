package com.lostandfound.controller;

import com.lostandfound.models.Item;
import com.lostandfound.service.SearchService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin
@RestController
@RequestMapping("/api/search")
public class SearchController {

    @Autowired
    private SearchService searchService;

    @GetMapping
    public List<Item> searchItems(@RequestParam String query) {
        return searchService.searchByTitle(query);
    }

    @GetMapping("/status/{status}")
    public List<Item> getItemsByStatus(@PathVariable String status) {
        return searchService.getItemsByStatus(status.toUpperCase());
    }
}
