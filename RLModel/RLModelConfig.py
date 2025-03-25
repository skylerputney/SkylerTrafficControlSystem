# Map of intersection ID to PLC Tag
intersections_map = {
    0: "OxU",  # Oakland St crosses University Ave
    1: "UxE",  # University Ave crosses Evansdale Dr
    2: "PxU",  # Patteson Dr crosses University Ave
    3: "PxK",  # Patteson Dr crosses Kroger
    4: "PxM",  # Patteson Dr crosses Morrill Way
    5: "MxP",  # Monongahela Blvd crosses Patteson Dr
    6: "MxE",  # Monongahela Blvd crosses Evansdale Dr
    7: "ExM",  # Evansdale Dr crosses Morrill Way -> assumed Evansdale X FineArts
    8: "MxR"  # Morrill Way crosses Rec Center Dr
}

# Map of detector ID to ???camera input???
detectors_map = {

}

# Map of intersection(s) to detector(s)
intersection_detectors_map = {
    0: [0, 1, 2, 3]  # Intersection 0 has detectors 0-3
}