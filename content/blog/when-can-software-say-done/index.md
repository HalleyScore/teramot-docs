---
title: "When Can Software Honestly Say Done?"
date: 2026-10-13T09:00:00-03:00
draft: false
authors:
  - valentin-torassa
tags:
  - reliability
  - data
  - product-engineering
categories:
  - engineering
summary: "A source disappeared from the screen while its job kept running. What we changed taught us to take the word ‘done’ seriously."
showTableOfContents: true
---

You press **Delete**. The thing disappears. That should be the boring end of the story.

At Teramot, a data source has a life in the product and another in the system that does the actual data work. We found a case where the product erased its copy after the other system failed to delete its own. The source was gone from the screen. Its scheduled job kept running.

<figure class="tm-done-figure" aria-labelledby="tm-done-split-caption">
  <div class="tm-done-split">
    <div class="tm-done-split-top"><span>ONE CLICK</span><span>DELETE SOURCE ↗</span></div>
    <div class="tm-done-split-grid">
      <div class="tm-done-split-cell">
        <span class="tm-done-kicker">WHAT THE SCREEN SAID</span>
        <strong>Gone.</strong>
        <span class="tm-done-small">The source was no longer listed.</span>
      </div>
      <div class="tm-done-split-cell tm-done-split-cell-live">
        <span class="tm-done-kicker">WHAT THE ENGINE DID</span>
        <strong>Still running.</strong>
        <span class="tm-done-small">A scheduled ingestion continued.</span>
      </div>
    </div>
  </div>
  <figcaption id="tm-done-split-caption">The same source had two different endings.</figcaption>
</figure>

That gap matters even if you never think about the machinery behind the button. The person who deleted the source had no reason to expect more work from it. And with its entry gone from the product, there was no obvious way to try the deletion again.

## One button speaks for more than one system

The person sees one action. Behind it, Teramot must tell the data engine to remove its source, then remove the record that makes that source visible and manageable in the product.

The old path handled one awkward case badly: a source whose first setup had not finished. If the engine could not remove it, Aleph wrote a warning and carried on deleting its own record. The warning was useful to an engineer reading logs. It did nothing for the person looking at an empty source list.

I like to think of this as a receipt problem. Sending a request is the equivalent of asking a restaurant to cancel an order. Removing the order from your app before the kitchen acknowledges it does not stop dinner from arriving.

<figure class="tm-done-figure" aria-labelledby="tm-done-path-caption">
  <div class="tm-done-paths">
    <div class="tm-done-path">
      <span class="tm-done-path-label">BEFORE</span>
      <span class="tm-done-path-step">Ask the engine to delete</span>
      <span class="tm-done-path-arrow">↓</span>
      <span class="tm-done-path-step tm-done-path-step-warn">The engine cannot confirm</span>
      <span class="tm-done-path-arrow">↓</span>
      <strong class="tm-done-path-result tm-done-path-result-bad">Remove the product record anyway</strong>
    </div>
    <div class="tm-done-path tm-done-path-now">
      <span class="tm-done-path-label">NOW</span>
      <span class="tm-done-path-step">Ask the engine to delete</span>
      <span class="tm-done-path-arrow">↓</span>
      <span class="tm-done-path-step tm-done-path-step-warn">The engine cannot confirm</span>
      <span class="tm-done-path-arrow">↓</span>
      <strong class="tm-done-path-result tm-done-path-result-good">Keep the source visible for a retry</strong>
    </div>
  </div>
  <figcaption id="tm-done-path-caption">The change was where the process stops when an answer is missing.</figcaption>
</figure>

## We changed what happens when the answer is missing

Aleph now keeps the source record when it cannot confirm that the engine removed its copy. If it cannot find the engine's source, it tells the caller the source was not deleted and can be retried. If the engine refuses the deletion, the process stops and reports the failure. When the engine confirms deletion, Aleph can remove its own record.

We tested the paths where the engine fails or times out, and checked that the source remains available for another attempt. The successful path still removes it. This was a small change to the code, but a larger change to what the product is willing to claim.

<div class="tm-done-rule"><span>THE RULE</span><p>Keep the handle until the work it controls is finished.</p></div>

## The meaning of done

“Done” is a statement about the world beyond the screen. A source disappearing from a list is something the product can do by itself. Stopping the work behind that source requires an answer from the system doing it.

Sometimes that answer is “try again.” That is useful information: the source is still visible, the next action is possible, and nobody has to discover a running job by accident. In our case, that honesty is what keeps a failed delete from turning into an invisible one.

*— Valentín Torassa*
