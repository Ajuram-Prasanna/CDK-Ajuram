#!/usr/bin/env python3
import aws_cdk as cdk
from stacks.pipeline_stack import CdkSampleStack

app = cdk.App()


dev_account = app.node.try_get_context("dev")["account"]
dev_region = app.node.try_get_context("dev")["region"]
prod_account = app.node.try_get_context("prod")["account"]
prod_region = app.node.try_get_context("prod")["region"]

config = {dev_account, dev_region, prod_account, prod_region}

CdkSampleStack(app, "CdkSampleStack", config)
app.synth()