package com.stockTracker.congressWatch.importer.modles;

import org.springframework.data.mongodb.core.mapping.Document;

import java.util.Objects;


@Document(collation = "stockTransactions")
public class StockTransaction {
    private int disclosureYear;
    private String disclosure_date;
    private String transaction_date;
    private String owner;
    private String ticker;
    private String asset_description;
    private String type;
    // TODO: There will be some normalization for this
    private String amount;
    private String representative;
    private String district;
    private String ptr_link;
    private boolean cap_gains_over_200_usd;

    public StockTransaction() {
    }

    public int getDisclosureYear() {
        return disclosureYear;
    }

    public void setDisclosureYear(int disclosureYear) {
        this.disclosureYear = disclosureYear;
    }

    public String getDisclosure_date() {
        return disclosure_date;
    }

    public void setDisclosure_date(String disclosure_date) {
        this.disclosure_date = disclosure_date;
    }

    public String getTransaction_date() {
        return transaction_date;
    }

    public void setTransaction_date(String transaction_date) {
        this.transaction_date = transaction_date;
    }

    public String getOwner() {
        return owner;
    }

    public void setOwner(String owner) {
        this.owner = owner;
    }

    public String getTicker() {
        return ticker;
    }

    public void setTicker(String ticker) {
        this.ticker = ticker;
    }

    public String getAsset_description() {
        return asset_description;
    }

    public void setAsset_description(String asset_description) {
        this.asset_description = asset_description;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getAmount() {
        return amount;
    }

    public void setAmount(String amount) {
        this.amount = amount;
    }

    public String getRepresentative() {
        return representative;
    }

    public void setRepresentative(String representative) {
        this.representative = representative;
    }

    public String getDistrict() {
        return district;
    }

    public void setDistrict(String district) {
        this.district = district;
    }

    public String getPtr_link() {
        return ptr_link;
    }

    public void setPtr_link(String ptr_link) {
        this.ptr_link = ptr_link;
    }

    public boolean isCap_gains_over_200_usd() {
        return cap_gains_over_200_usd;
    }

    public void setCap_gains_over_200_usd(boolean cap_gains_over_200_usd) {
        this.cap_gains_over_200_usd = cap_gains_over_200_usd;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        StockTransaction that = (StockTransaction) o;
        return disclosureYear == that.disclosureYear && cap_gains_over_200_usd == that.cap_gains_over_200_usd && Objects.equals(disclosure_date, that.disclosure_date) && Objects.equals(transaction_date, that.transaction_date) && Objects.equals(owner, that.owner) && Objects.equals(ticker, that.ticker) && Objects.equals(asset_description, that.asset_description) && Objects.equals(type, that.type) && Objects.equals(amount, that.amount) && Objects.equals(representative, that.representative) && Objects.equals(district, that.district) && Objects.equals(ptr_link, that.ptr_link);
    }

    @Override
    public int hashCode() {
        return Objects.hash(disclosureYear, disclosure_date, transaction_date, owner, ticker, asset_description, type, amount, representative, district, ptr_link, cap_gains_over_200_usd);
    }
}