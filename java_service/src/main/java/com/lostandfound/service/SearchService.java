package com.lostandfound.service;

import com.lostandfound.models.Item;
import com.lostandfound.repository.ItemRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class SearchService {

    @Autowired
    private ItemRepository itemRepository;

    public List<Item> searchByTitle(String query) {
        return itemRepository.findByTitleContainingIgnoreCase(query);
    }

    public List<Item> getItemsByStatus(String status) {
        return itemRepository.findByStatus(status);
    }
}
