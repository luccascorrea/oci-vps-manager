from plugins.ip_security.backends.base import IPRulesBackend, CurrentCidr
import oci


class OracleCloudBackend(IPRulesBackend):
    def __init__(self, auth: "dict"):
        self.client = oci.core.VirtualNetworkClient(auth)

    def update_rules(self, rules_info: "dict", new_cidr: str):
        security_lists = rules_info["security_lists"]
        for security_list_config in security_lists:
            # Get current rules
            security_list_id = security_list_config["security_list_id"]
            response = self.client.get_security_list(security_list_id=security_list_id)
            assert response is not None
            security_list = response.data
            rules_config = security_list_config["rules"]
            rules_description_map = {
                rule.description: rule
                for rule in security_list.ingress_security_rules
                if rule.description
            }
            changed = False
            for rule_config in rules_config:
                rule = rules_description_map[rule_config["description"]]
                if rule.source != new_cidr:
                    rule.source = new_cidr
                    changed = True

            if changed:
                self.client.update_security_list(
                    security_list_id=security_list_id,
                    update_security_list_details=security_list,
                )

    def get_current_cidrs(self, rules_info: "dict") -> list[CurrentCidr]:
        security_lists = rules_info["security_lists"]
        cidrs = []
        for security_list_config in security_lists:
            security_list_id = security_list_config["security_list_id"]
            response = self.client.get_security_list(security_list_id=security_list_id)
            assert response is not None
            security_list = response.data

            rules_config = security_list_config["rules"]
            rules_description_map = {
                rule.description: rule
                for rule in security_list.ingress_security_rules
                if rule.description
            }
            for rule_config in rules_config:
                rule = rules_description_map[rule_config["description"]]
                cidrs.append(
                    {
                        "current_cidr": rule.source,
                        "description": rule_config["label"],
                    }
                )

        return cidrs
