def compare_schemas(source_schema, target_schema):
    report = {
        "missing_fields": [],
        "type_mismatches": [],
        "new_fields_in_target": []
    }

    src_fields = source_schema.get("fields", {})
    tgt_fields = target_schema.get("fields", {})

    for field in src_fields:
        if field not in tgt_fields:
            report["missing_fields"].append(field)

    for field in src_fields:
        if field in tgt_fields:
            if set(src_fields[field]) != set(tgt_fields[field]):
                report["type_mismatches"].append({
                    "field": field,
                    "source": src_fields[field],
                    "target": tgt_fields[field]
                })

    for field in tgt_fields:
        if field not in src_fields:
            report["new_fields_in_target"].append(field)

    return report


def compare_indexes(source_indexes, target_indexes):
    def normalize(idx):
        return {
            "key": idx.get("key"),
            "unique": idx.get("unique", False)
        }

    src = [normalize(i) for i in source_indexes]
    tgt = [normalize(i) for i in target_indexes]

    return {
        "missing_indexes": [i for i in src if i not in tgt],
        "extra_indexes": [i for i in tgt if i not in src]
    }