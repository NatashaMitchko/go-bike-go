package main

import (
	"encoding/json"
	"log"
	"net/http"
    "fmt"
)

type StationInfo struct {
	LastUpdated int `json:"last_updated"`
	TTL         int `json:"ttl"`
	Data        struct {
		Stations []struct {
			StationID             string   `json:"station_id"`
			Name                  string   `json:"name"`
			ShortName             string   `json:"short_name"`
			Lat                   float64  `json:"lat"`
			Lon                   float64  `json:"lon"`
			RegionID              int      `json:"region_id"`
			RentalMethods         []string `json:"rental_methods"`
			Capacity              int      `json:"capacity"`
			EightdHasKeyDispenser bool     `json:"eightd_has_key_dispenser"`
		} `json:"stations"`
	} `json:"data"`
}
    type StationStatus struct {
    LastUpdated int `json:"last_updated"`
    TTL int `json:"ttl"`
    Data struct {
        Stations []struct {
            StationID string `json:"station_id"`
            NumBikesAvailable int `json:"num_bikes_available"`
            NumBikesDisabled int `json:"num_bikes_disabled"`
            NumDocksAvailable int `json:"num_docks_available"`
            NumDocksDisabled int `json:"num_docks_disabled"`
            IsInstalled int `json:"is_installed"`
            IsRenting int `json:"is_renting"`
            IsReturning int `json:"is_returning"`
            LastReported int `json:"last_reported"`
            EightdHasAvailableKeys bool `json:"eightd_has_available_keys"`
        } `json:"stations"`
    } `json:"data"`
}

func main() {
    const stationURL = "https://gbfs.citibikenyc.com/gbfs/en/station_information.json"
    resp, err := http.Get(stationURL)
    if err != nil {
        log.Fatal(err)
    }
    defer resp.Body.Close()
    var si StationInfo
    if err := json.NewDecoder(resp.Body).Decode(&si); err != nil {
        log.Fatal(err)
    }
    // for _, s := range si.Data.Stations {
    //     fmt.Println(s.Name)
    // }

    const stationStatusURL = "https://gbfs.citibikenyc.com/gbfs/en/station_status.json"
    resp, err = http.Get(stationStatusURL)
    if err != nil {
        log.Fatal(err)
    }
    defer resp.Body.Close()
    var ss StationStatus
    if err := json.NewDecoder(resp.Body).Decode(&ss); err != nil {
        log.Fatal(err)
    }

    for _, s := range ss.Data.Stations {
        fmt.Println(s.StationID, "", s.NumBikesAvailable)
    }

}
