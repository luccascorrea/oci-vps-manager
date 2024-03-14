from typing import Dict, TypedDict

from botocore.client import ClientError
from plugins.ip_security.backends.base import IPRulesBackend, CurrentCidr
import boto3


class AWSRule(TypedDict):
    port: int
    rule_id: str
    description: str
    label: str


class AWSGroupInfo(TypedDict):
    group_id: str
    rules: list[AWSRule]

class AWSRulesInfo(TypedDict):
    groups: list[AWSGroupInfo]


class AWSBackend(IPRulesBackend):
    def __init__(self, auth: "Dict"):
        access_key_id = auth["access_key_id"]
        secret_access_key = auth["secret_access_key"]
        session = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=auth["region"],
        )
        self.client = session.client("ec2")

    def update_rules(self, rules_info: "AWSRulesInfo", new_cidr: str):
        for group_info in rules_info["groups"]:
            group_id = group_info["group_id"]
            rules = group_info["rules"]

            data = {"GroupId": group_id, "SecurityGroupRules": []}

            for rule in rules:
                data["SecurityGroupRules"].append(
                    {
                        "SecurityGroupRuleId": rule["rule_id"],
                        "SecurityGroupRule": {
                            "IpProtocol": "tcp",
                            "FromPort": rule["port"],
                            "ToPort": rule["port"],
                            "CidrIpv4": new_cidr,
                            "Description": rule["description"],
                        },
                    }
                )

            try:
                self.client.modify_security_group_rules(**data)
            except ClientError as e:
                if e.response["Error"]["Code"] == "InvalidPermission.Duplicate":
                    pass

    def get_current_cidrs(self, rules_info: "AWSRulesInfo") -> list[CurrentCidr]:
        rules = [val for group_info in rules_info["groups"] for val in group_info["rules"]]

        description_map = {rule["rule_id"]: rule["label"] for rule in rules}
        data = {"SecurityGroupRuleIds": [rule["rule_id"] for rule in rules]}

        response = self.client.describe_security_group_rules(**data)

        result = []
        for rule in response["SecurityGroupRules"]:
            rule_id = rule["SecurityGroupRuleId"]
            description = description_map[rule_id]
            result.append(
                {"current_cidr": rule["CidrIpv4"], "description": description}
            )

        return result
